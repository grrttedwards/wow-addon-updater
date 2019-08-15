import requests
import re
import random
from updater.site.abstract_site import AbstractSite


class Github(AbstractSite):
    _URL = 'https://github.com/'

    def __init__(self, url: str):
        super().__init__(url)

    @classmethod
    def get_supported_urls(cls):
        return [cls._URL]

    def find_zip_url(self):
        return self.url.replace('/tree/', '/archive/', 1) + '.zip'

    def get_latest_version(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            content = str(response.content)
            match = re.search(
                r'<a data-pjax.*?\/commit\/(?P<hash>.*?)">',
                content)
            result = ''
            if match:
                result = match.group('hash')[-8:] #Just use the last 8 chars of the hash, same as Tukui.
            return result.strip()
        except Exception:
            print(f"Failed to find version number for: {self.url}")
            raise
    
    def get_addon_name(self):
        addon_name = AbstractSite.get_addon_name(self)
        addon_name = re.search(r".*?\/(?P<name>.+?)\/", addon_name).group('name')
        return addon_name