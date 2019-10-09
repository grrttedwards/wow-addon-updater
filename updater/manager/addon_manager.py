import configparser
import platform
import shutil
import subprocess
import tempfile
import threading
import zipfile
from io import BytesIO
from os.path import isfile, isdir, join

import requests
from requests import HTTPError

from updater.site import site_handler, github
from updater.site.abstract_site import SiteError, AbstractSite
from updater.site.enum import GameVersion
from updater.manager.config import Config


def error(message: str):
    print(message)
    exit(1)


class AddonManager:
    _UNAVAILABLE = 'Unavailable'

    def __init__(self, config_file):
        self.manifest = []
        self.config = Config(config_file)

    def update_all(self):
        threads = []

        with open(self.config.addon_list_file, 'r') as fin:
            addon_entries = fin.read().splitlines()

        # filter any blank lines or lines commented with an octothorp (#)
        addon_entries = [
            entry for entry in addon_entries if entry and not entry.startswith('#')]

        for addon_entry in addon_entries:
            thread = threading.Thread(
                target=self.update_addon, args=(addon_entry,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.set_installed_versions()
        self.display_results()

    def update_addon(self, addon_entry):
        # Expected format: "mydomain.com/myaddon" or "mydomain.com/myaddon|subfolder"
        addon_url, *subfolder = addon_entry.split('|')

        site = site_handler.get_handler(addon_url, self.config.game_version)

        addon_name = site.get_addon_name()

        if subfolder:
            [subfolder] = subfolder
            addon_name = f"{addon_name}|{subfolder}"

        try:
            latest_version = site.get_latest_version()
        except SiteError as e:
            print(e)
            latest_version = AddonManager._UNAVAILABLE

        installed_version = self.get_installed_version(addon_name)
        if latest_version == AddonManager._UNAVAILABLE:
            pass
        elif latest_version == installed_version:
            print(f"{addon_name} version {installed_version} is up to date.\n")
        else:
            print(
                f"Installing/updating addon: {addon_name} to version: {latest_version}...\n")

            try:
                zip_url = site.find_zip_url()
                addon_zip = self.get_addon_zip(site.session, zip_url)
                self.extract_to_addons(addon_zip, subfolder, site)
            except HTTPError:
                print(f"Failed to download zip for [{addon_name}]")
                latest_version = AddonManager._UNAVAILABLE
            except KeyError:
                print(
                    f"Failed to extract subfolder [{subfolder}] in archive for [{addon_name}]")
                latest_version = AddonManager._UNAVAILABLE
            except SiteError as e:
                print(e)
                latest_version = AddonManager._UNAVAILABLE
            except Exception as e:
                print(f"Unexpected error unzipping [{addon_name}]")
                latest_version = AddonManager._UNAVAILABLE

        addon_entry = [addon_name, addon_url,
                       installed_version, latest_version]
        self.manifest.append(addon_entry)

    def get_addon_zip(self, session: requests.Session, zip_url):
        r = session.get(zip_url, stream=True)
        r.raise_for_status()  # Raise an exception for HTTP errors
        return zipfile.ZipFile(BytesIO(r.content))

    def extract_to_addons(self, zipped: zipfile.ZipFile, subfolder, site: AbstractSite):
        if isinstance(site, github.GitHub) or subfolder:
            first_zip_member, *_ = zipped.namelist()
            # sometimes zip files don't contain an entry for the top-level folder, so parse it from the first member
            top_level_folder, *_ = first_zip_member.split('/')
            with tempfile.TemporaryDirectory() as temp_dir:
                # unfortunately include some github-specific folder logic here... think about how to refactor this
                if '-master' in top_level_folder:
                    destination_dir = join(
                        self.config.wow_addon_location, top_level_folder.replace('-master', ''))
                    temp_source_dir = join(temp_dir, top_level_folder)
                if subfolder:
                    destination_dir = join(
                        self.config.wow_addon_location, subfolder)
                    temp_source_dir = join(
                        temp_dir, top_level_folder, subfolder)
                zipped.extractall(path=temp_dir)
                if not isdir(temp_source_dir):
                    raise KeyError()
                if isdir(destination_dir):
                    shutil.rmtree(destination_dir)
                shutil.copytree(src=temp_source_dir, dst=destination_dir)
        else:
            zipped.extractall(path=self.config.wow_addon_location)

    def get_installed_version(self, addon_name):
        installed_vers = configparser.ConfigParser()
        installed_vers.read(self.config.installed_vers_file)
        try:
            return installed_vers.get(addon_name, 'version')
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None

    def set_installed_versions(self):
        versions = {}
        for (addon_name, addon_url, _, new_version) in sorted(self.manifest):
            if new_version != AddonManager._UNAVAILABLE:
                versions[addon_name] = {
                    "url": addon_url, "version": new_version}

        installed_versions = configparser.ConfigParser()
        installed_versions.read_dict(versions)
        with open(self.config.installed_vers_file, 'wt') as installed_versions_file:
            installed_versions.write(installed_versions_file)

    def display_results(self):
        headers = [["Name", "Prev. Version", "New Version"],
                   ["─" * 4, "─" * 13, "─" * 11]]
        table = [[name,
                  "-----" if prev is None else prev,
                  "Up to date" if new == prev else new]
                 for name, _, prev, new in self.manifest]  # eliminate the URL
        results = headers + table
        col_width = max(len(word)
                        for row in results for word in row) + 2  # padding
        print()
        for row in results:
            print("".join(word.ljust(col_width) for word in row))
