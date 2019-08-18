import re

import requests

from updater.site.abstract_site import AbstractSite, SiteError


class Github(AbstractSite):
    _URL = 'https://github.com/'

    def __init__(self, url: str):
        if '/tree/master' not in url:
            url = (url + '/tree/master')
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
            version = re.search(
                r"<a data-pjax.*?/commit/(?P<hash>.*?)\">",
                content).group('hash')
            return version[:7]  # truncate the hash to the first 7 digits
        except Exception:
            raise SiteError(f"Failed to find version number for: {self.url}")

    def get_addon_name(self):
        addon_name = AbstractSite.get_addon_name(self)
        addon_name = re.search(r".*?/(?P<name>.+?)/", addon_name).group('name')
        return addon_name
