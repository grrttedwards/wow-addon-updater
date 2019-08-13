import re

import requests

from updater.site.AbstractSite import AbstractSite


class Tukui(AbstractSite):
    _URL = 'https://git.tukui.org/elvui/'

    def __init__(self, url: str):
        super().__init__(url)

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
            match = re.search(
                r'data-title="Copy commit SHA to clipboard".*data-clipboard-text="(?P<hash>[a-f0-9]{40}?)"',
                content)
            result = ''
            if match:
                result = match.group('hash')
            return result.strip()
        except Exception:
            print(f"Failed to find version number for: {self.url}")
            raise
