import re

import requests

from updater.site.abstract_site import AbstractSite
from updater.site.enum import GameVersion


class WoWInterface(AbstractSite):
    _URL = 'https://www.wowinterface.com/downloads/'

    def __init__(self, url: str, game_version: GameVersion):
        if game_version is GameVersion.classic:
            raise NotImplementedError("Updating classic addons are not yet supported for WoWAce.")
        super().__init__(url, game_version)

    @classmethod
    def get_supported_urls(cls) -> [str]:
        return [cls._URL]

    def find_zip_url(self):
        downloadpage = self.url.replace('info', 'download')
        try:
            page = requests.get(downloadpage + '/download')
            page.raise_for_status()  # Raise an exception for HTTP errors
            content_string = str(page.content)
            index_of_ziploc = content_string.find('Problems with the download? <a href="') + 37  # first char of the url
            end_quote = content_string.find('"', index_of_ziploc)  # ending quote after the url
            return content_string[index_of_ziploc:end_quote]
        except Exception as e:
            raise self.download_error() from e

    def get_latest_version(self):
        try:
            page = requests.get(self.url)
            page.raise_for_status()  # Raise an exception for HTTP errors
            content_string = str(page.content)
            index_of_ver = content_string.find('id="version"') + 22  # first char of the version string
            end_tag = content_string.find('</div>', index_of_ver)  # ending tag after the version string
            return content_string[index_of_ver:end_tag].strip()
        except Exception as e:
            raise self.version_error() from e

    def get_addon_name(self):
        addon_name = AbstractSite.get_addon_name(self)
        addon_name = re.search(r"info[0-9]+-(?P<name>[a-zA-z0-9]+)\.html", addon_name).group('name')
        return addon_name
