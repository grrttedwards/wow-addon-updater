import configparser
import threading
import zipfile
from io import BytesIO
from os.path import isfile, join

import requests
from requests import HTTPError

from updater.site import SiteHandler

CHANGELOG_URL = 'https://raw.githubusercontent.com/grrttedwards/wow-addon-updater/master/changelog.txt'
CHANGELOG_FILE = 'changelog.txt'
NEW_UPDATE_MESSAGE = 'A new update is available! Check it out at https://github.com/grrttedwards/wow-addon-updater !'


def confirm_exit():
    input('\nPress the Enter key to exit')
    exit(0)


def check_version():
    if isfile(CHANGELOG_FILE):
        downloaded_changelog = requests.get(CHANGELOG_URL).text
        with open(CHANGELOG_FILE, mode='r') as f:
            current_changelog = f.read()
        if downloaded_changelog != current_changelog:
            print(NEW_UPDATE_MESSAGE)


class AddonManager:
    UNAVAILABLE = 'Unavailable'

    def __init__(self):
        self.manifest = []

        # Read config file
        if not isfile('config.ini'):
            print("Failed to read configuration file. Are you sure there is a file called 'config.ini'?")
            confirm_exit()

        config = configparser.ConfigParser()
        config.read('config.ini')

        try:
            self.WOW_ADDON_LOCATION = config['WOW ADDON UPDATER']['WoW Addon Location']
            self.ADDON_LIST_FILE = config['WOW ADDON UPDATER']['Addon List File']
            self.INSTALLED_VERS_FILE = config['WOW ADDON UPDATER']['Installed Versions File']
            self.AUTO_CLOSE = config['WOW ADDON UPDATER']['Close Automatically When Completed']
        except Exception:
            print("Failed to parse configuration file. Are you sure it is formatted correctly?")
            confirm_exit()

        if not isfile(self.ADDON_LIST_FILE):
            print("Failed to read addon list file. Are you sure the file exists?")
            confirm_exit()

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
        addon_url, *_ = addon_entry.split('|')

        addon_name = SiteHandler.get_addon_name(addon_entry)
        try:
            latest_version = SiteHandler.get_latest_version(addon_url)
        except Exception:
            print(f"Failed to retrieve latest version for {addon_name}.\n")
            latest_version = AddonManager.UNAVAILABLE

        installed_version = self.get_installed_version(addon_name)
        if latest_version == AddonManager.UNAVAILABLE:
            pass
        elif latest_version == installed_version:
            print(f"{addon_name} version {latest_version} is up to date.\n")
        else:
            print(f"Installing/updating addon: {addon_name} to version: {latest_version}...\n")

            try:
                zip_url = SiteHandler.find_zip_url(addon_url)
                _, *subfolder = addon_name.split('|')
                addon_zip = self.get_addon_zip(zip_url)
                self.extract_to_addons(addon_zip, subfolder)
            except HTTPError:
                print(f"Failed to download zip for [{addon_name}]")
            except KeyError:
                print(f"Failed to find subfolder [{subfolder}] in archive for [{addon_name}]")

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
            if new_version != AddonManager.UNAVAILABLE:
                versions[addon_name] = {"url": addon_url, "version": new_version}

        installed_versions = configparser.ConfigParser()
        installed_versions.read_dict(versions)
        with open(self.INSTALLED_VERS_FILE, 'wt') as installed_versions_file:
            installed_versions.write(installed_versions_file)

    def display_results(self):
        if self.AUTO_CLOSE == 'False':
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
            confirm_exit()
