import configparser
import logging
import platform
import shutil
import subprocess
import tempfile
import zipfile
from io import BytesIO
from multiprocessing.pool import ThreadPool
from os.path import isfile, isdir, join

import requests
from requests import HTTPError

from updater.site import site_handler, github, tukui
from updater.site.abstract_site import SiteError, AbstractSite
from updater.site.enum import GameVersion

logger = logging.getLogger(__name__)


def error(message: str):
    logger.error(message)
    exit(1)


def normalize_path(path: str) -> str:
    env = platform.platform().lower()
    if 'linux' in env and 'microsoft' in env:
        return subprocess.check_output(['wslpath', path], text=True)
    return path


class AddonManager:
    _UNAVAILABLE = 'Unavailable'

    def __init__(self, config_file):
        self.manifest = []

        # Read config file
        if not isfile(config_file):
            error(f"Failed to read config file. Are you sure there is a file called {config_file}?")

        config = configparser.ConfigParser()
        config.read(config_file)

        try:
            self.wow_addon_location = config['WOW ADDON UPDATER']['WoW Addon Location']
            self.addon_list_file = config['WOW ADDON UPDATER']['Addon List File']
            self.installed_vers_file = config['WOW ADDON UPDATER']['Installed Versions File']
            self.game_version = GameVersion[config['WOW ADDON UPDATER']['Game Version']]
        except Exception:
            error("Failed to parse configuration file. Are you sure it is formatted correctly?")

        if not isfile(self.addon_list_file):
            error(f"Failed to read addon list file ({self.addon_list_file}). Are you sure the file exists?")

        self.wow_addon_location = normalize_path(self.wow_addon_location)
        if not isdir(self.wow_addon_location):
            error(f"Could not find addon directory ({self.wow_addon_location}). Are you sure it exists?")

    def update_all(self):
        with open(self.addon_list_file, 'r') as fin:
            addon_entries = fin.read().splitlines()

        # filter any blank lines or lines commented with an octothorp (#)
        addon_entries = [entry for entry in addon_entries if entry and not entry.startswith('#')]

        # chose an arbitrary reasonable number of threads
        pool = ThreadPool(10)
        for addon_entry in addon_entries:
            pool.apply_async(self.update_addon, args=(addon_entry,))
        pool.close()
        pool.join()

        self.set_installed_versions()
        self.display_results()
        self.explain_curse_error()

    def update_addon(self, addon_entry):
        # Expected format: "mydomain.com/myaddon" or "mydomain.com/myaddon|subfolder"
        addon_url, *subfolder = addon_entry.split('|')

        site = site_handler.get_handler(addon_url, self.game_version)

        try:
            addon_name = site.get_addon_name()
        except Exception as e:
            logger.exception(e)

        if subfolder:
            [subfolder] = subfolder
            addon_name = f"{addon_name}|{subfolder}"

        try:
            latest_version = site.get_latest_version()
        except SiteError as e:
            logger.exception(e)
            latest_version = AddonManager._UNAVAILABLE

        installed_version = self.get_installed_version(addon_name)
        if latest_version in [AddonManager._UNAVAILABLE, installed_version]:
            pass
        else:
            logger.info(f"Installing/updating addon: {addon_name} to version: {latest_version}...\n")

            try:
                zip_url = site.find_zip_url()
                addon_zip = self.get_addon_zip(site.session, zip_url)
                self.extract_to_addons(addon_zip, subfolder, site)
            except HTTPError:
                logger.exception(f"Failed to download zip for [{addon_name}]")
                latest_version = AddonManager._UNAVAILABLE
            except KeyError:
                logger.exception(f"Failed to extract subfolder [{subfolder}] in archive for [{addon_name}]")
                latest_version = AddonManager._UNAVAILABLE
            except SiteError as e:
                logger.exception(e)
                latest_version = AddonManager._UNAVAILABLE
            except Exception as e:
                logger.exception(f"Unexpected error unzipping [{addon_name}]")
                latest_version = AddonManager._UNAVAILABLE

        addon_entry = [addon_name, addon_url, installed_version, latest_version]
        self.manifest.append(addon_entry)

    def get_addon_zip(self, session: requests.Session, zip_url):
        r = session.get(zip_url, stream=True)
        r.raise_for_status()  # Raise an exception for HTTP errors
        return zipfile.ZipFile(BytesIO(r.content))

    def extract_to_addons(self, zipped: zipfile.ZipFile, subfolder, site: AbstractSite):
        with tempfile.TemporaryDirectory() as temp_dir:
            norm_src_dir = temp_dir
            destination_dir = self.wow_addon_location

            if isinstance(site, github.GitHub):
                first_zip_member, *_ = zipped.namelist()
                # sometimes zips don't contain an entry for the top-level folder, so parse it from the first member
                top_level_folder, *_ = first_zip_member.split('/')

                destination_dir = join(self.wow_addon_location, top_level_folder.replace('-master', ''))
                norm_src_dir = join(temp_dir, top_level_folder)

            if subfolder:
                destination_dir = join(self.wow_addon_location, subfolder)
                norm_src_dir = join(norm_src_dir, subfolder)

            if subfolder or isinstance(site, github.GitHub):
                zipped.extractall(path=temp_dir)
                if not isdir(norm_src_dir):
                    raise KeyError()
                if isdir(destination_dir):
                    shutil.rmtree(destination_dir)
                shutil.copytree(src=norm_src_dir, dst=destination_dir)
            else:
                # no subfolder and no folder renaming needed, just copy the entire archive contents as-is
                zipped.extractall(path=self.wow_addon_location)

    def get_installed_version(self, addon_name):
        installed_vers = configparser.ConfigParser()
        installed_vers.read(self.installed_vers_file)
        try:
            return installed_vers.get(addon_name, 'version')
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None

    def set_installed_versions(self):
        versions = {}
        for (addon_name, addon_url, _, new_version) in sorted(self.manifest):
            if new_version != AddonManager._UNAVAILABLE:
                versions[addon_name] = {"url": addon_url, "version": new_version}

        installed_versions = configparser.ConfigParser()
        installed_versions.read_dict(versions)
        with open(self.installed_vers_file, 'wt') as installed_versions_file:
            installed_versions.write(installed_versions_file)

    def display_results(self):
        headers = [["Name", "Prev. Version", "New Version"],
                   ["─" * 4, "─" * 13, "─" * 11]]
        table = [[name,
                  "-----" if prev is None else prev,
                  "Up to date" if new == prev else new]
                 for name, _, prev, new in self.manifest]  # eliminate the URL
        results = headers + table
        col_width = max(len(word) for row in results for word in row) + 2  # padding
        results = ["".join(word.ljust(col_width) for word in row) for row in results]
        logger.info('\n\n' + '\n'.join(results))

    def explain_curse_error(self):
        for _, url, _, new in self.manifest:
            if "curse" in url and new == "Unavailable":
                message = '\n'.join([
                    "Looks like Curse may be blocking your requests!  :(",
                    "This tool relies on a third party module to look like a browser and not a script.",
                    "Try running 'pipenv update' on your command line and trying again.",
                    "If it doesn't help, feel free to open an issue on GitHub."
                ])
                logger.info('\n\n' + message)
                return
