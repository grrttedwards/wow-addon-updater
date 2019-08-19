import re

import requests

from updater.site.abstract_site import AbstractSite
from updater.site.enum import GameVersion


class Tukui(AbstractSite):
    _URL = 'https://git.tukui.org/elvui/'

    def __init__(self, url: str):
        super().__init__(url, GameVersion.agnostic)

    @classmethod
    def get_supported_urls(cls) -> [str]:
        return [cls._URL]

    def find_zip_url(self):
        return self.url + '/-/archive/master/elvui-master.zip'

    def get_latest_version(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            content = str(response.content)
            version = re.search(
                r'data-title="Copy commit SHA to clipboard".*data-clipboard-text="(?P<hash>[a-f0-9]{40}?)"',
                content).group('hash')
            return version[:7]  # truncate the hash to the first 7 digits
        except Exception as e:
            raise self.version_error() from e
