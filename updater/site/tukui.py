import requests
from bs4 import BeautifulSoup

from updater.site.abstract_site import AbstractSite
from updater.site.enum import GameVersion


class Tukui(AbstractSite):
    _URL = 'https://git.tukui.org/elvui/'
    latest_version = None

    session = requests.session()

    def __init__(self, url: str):
        super().__init__(url, GameVersion.agnostic)

    @classmethod
    def get_supported_urls(cls) -> [str]:
        return [cls._URL]

    def find_zip_url(self):
        version = self.get_latest_version()
        # like https://git.tukui.org/elvui/elvui/-/archive/v11.21/elvui-v11.21.zip
        return f"{self.url}/-/archive/{version}/{self.get_addon_name()}-{version}.zip"

    def get_latest_version(self):
        if self.latest_version:
            return self.latest_version
        try:
            response = Tukui.session.get(self.url + '/-/tags')
            response.raise_for_status()
            tags_page = BeautifulSoup(response.text, 'html.parser')
            version = tags_page.find('div', {'class': 'tags'}).find('a').string
        except Exception as e:
            raise self.version_error() from e
        self.latest_version = version
        return self.latest_version
