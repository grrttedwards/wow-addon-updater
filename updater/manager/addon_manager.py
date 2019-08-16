import configparser
import threading
import zipfile
from io import BytesIO
from os.path import isfile, join

import requests
from requests import HTTPError

from updater.site import site_handler


def error(message: str):
    print(message)
    exit(1)


class AddonManager:
    _UNAVAILABLE = 'Unavailable'
    _CONFIG_FILE = 'config.ini'

    def __init__(self):
        self.manifest = []

        # Read config file
        if not isfile(AddonManager._CONFIG_FILE):
            error(f"Failed to read config file. Are you sure there is a file called {AddonManager._CONFIG_FILE}?")

        config = configparser.ConfigParser()
        config.read(AddonManager._CONFIG_FILE)

        try:
            self.WOW_ADDON_LOCATION = config['WOW ADDON UPDATER']['WoW Addon Location']
            self.ADDON_LIST_FILE = config['WOW ADDON UPDATER']['Addon List File']
            self.INSTALLED_VERS_FILE = config['WOW ADDON UPDATER']['Installed Versions File']
        except Exception:
            error("Failed to parse configuration file. Are you sure it is formatted correctly?")

        if not isfile(self.ADDON_LIST_FILE):
            error(f"Failed to read addon list file ({self.ADDON_LIST_FILE}). Are you sure the file exists?")

    def update_all(self):
        threads = []

        with open(self.ADDON_LIST_FILE, 'r') as fin:
            addon_entries = fin.read().splitlines()

        for addon_entry in addon_entries:
            thread = threading.Thread(target=self.update_addon, args=(addon_entry,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.set_installed_versions()
        self.display_results()

    def update_addon(self, addon_entry):
        if not addon_entry or addon_entry.startswith('#'):
            return

        # Expected format: "mydomain.com/myzip.zip" or "mydomain.com/myzip.zip|subfolder"
        addon_url, *subfolder = addon_entry.split('|')

        site = site_handler.get_handler(addon_url)

        addon_name = site.get_addon_name()
        try:
            latest_version = site.get_latest_version()
        except Exception:
            print(f"Failed to retrieve latest version for {addon_name}.\n")
            latest_version = AddonManager._UNAVAILABLE

        installed_version = self.get_installed_version(addon_name)
        if latest_version == AddonManager._UNAVAILABLE:
            pass
        elif latest_version == installed_version:
            print(f"{addon_name} version {installed_version} is up to date.\n")
        else:
            print(f"Installing/updating addon: {addon_name} to version: {latest_version}...\n")

            try:
                zip_url = site.find_zip_url()
                addon_zip = self.get_addon_zip(zip_url)
                self.extract_to_addons(addon_zip, subfolder)
            except HTTPError:
                print(f"Failed to download zip for [{addon_name}]")
                latest_version = AddonManager._UNAVAILABLE
            except KeyError:
                print(f"Failed to find subfolder [{subfolder}] in archive for [{addon_name}]")
                latest_version = AddonManager._UNAVAILABLE
            except Exception:
                print(f"Unexpected error unzipping [{addon_name}]")
                latest_version = AddonManager._UNAVAILABLE

        addon_entry = [addon_name, addon_url, installed_version, latest_version]
        self.manifest.append(addon_entry)

    def get_addon_zip(self, zip_url):
        r = requests.get(zip_url, stream=True)
        r.raise_for_status()  # Raise an exception for HTTP errors
        return zipfile.ZipFile(BytesIO(r.content))

    def extract_to_addons(self, zipped: zipfile.ZipFile, subfolder):
        if subfolder:
            [subfolder] = subfolder
            destination_dir = join(self.WOW_ADDON_LOCATION, subfolder)
            zipped.extract(member=subfolder + '/', path=destination_dir)
        else:
            zipped.extractall(self.WOW_ADDON_LOCATION)

    def get_installed_version(self, addon_name):
        installed_vers = configparser.ConfigParser()
        installed_vers.read(self.INSTALLED_VERS_FILE)
        try:
            return installed_vers.get(addon_name, 'version')
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None

    def set_installed_versions(self):
        versions = {}
        for (addon_name, addon_url, _, new_version) in self.manifest:
            if new_version != AddonManager._UNAVAILABLE:
                versions[addon_name] = {"url": addon_url, "version": new_version}

        installed_versions = configparser.ConfigParser()
        installed_versions.read_dict(versions)
        with open(self.INSTALLED_VERS_FILE, 'wt') as installed_versions_file:
            installed_versions.write(installed_versions_file)

    def display_results(self):
        headers = [["Name", "Prev. Version", "New Version"],
                   ["-" * 4, "-" * 13, "-" * 11]]
        table = [[name,
                  "Not found" if prev is None else prev,
                  "Up to date" if new == prev else new]
                 for name, _, prev, new in self.manifest]  # eliminate the URL
        results = headers + table
        col_width = max(len(word) for row in results for word in row) + 2  # padding
        for row in results:
            print("".join(word.ljust(col_width) for word in row))
