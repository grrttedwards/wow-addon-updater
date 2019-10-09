from os.path import isfile, isdir
import configparser
import platform
import subprocess

from updater.site.enum import GameVersion


class Config:
    def __init__(self, config_file):
        # Read config file
        if not isfile(config_file):
            error(
                f"Failed to read config file. Are you sure there is a file called {config_file}?")

        # Extract config and check if required settings are set
        try:
            config = configparser.ConfigParser()
            config.read(config_file)
            config = config['WOW ADDON UPDATER']

            self.game_version = self.parse_game_version(config)
            self.wow_addon_location = self.parse_addon_location(config)
            self.addon_list_file = config.get('Addon List File', 'addons.txt')
            self.installed_vers_file = config.get(
                'Installed Versions File', 'installed.ini')
            self.self_update = self.parse_self_update(config)

        except Exception:
            error(
                'Failed to parse configuration file. Are you sure it is formatted correctly?')

        # Test if addon list exists
        if not isfile(self.addon_list_file):
            error(
                f"Failed to read addon list file ({self.addon_list_file}). Are you sure the file exists?")

    def parse_addon_location(self, config):
        wow_addon_location = config.get('WoW Addon Location')
        if wow_addon_location == None:
            error(
                'The location of the addon folder is missing from your configuration file.')

        # Normalize path for linux for windows clients
        wow_addon_location = normalize_path(wow_addon_location)

        if not isdir(wow_addon_location):
            error(
                f"Could not find addon directory ({self.wow_addon_location}). Are you sure it exists?")
        return wow_addon_location

    def parse_game_version(self, config):
        try:
            return GameVersion[config['Game Version']]
        except Exception:
            error(
                'The targeted game version is missing from your configuration file or invalid.')

    def parse_self_update(self, config):
        return str(config.get('Self Update')) in ['yes', 'true', 'y', '1']


def normalize_path(path: str) -> str:
    env = platform.platform().lower()
    if 'linux' in env and 'microsoft' in env:
        return subprocess.check_output(['wslpath', path], text=True)
    return path


def error(message: str):
    print(message)
    exit(1)
