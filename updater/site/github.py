import requests
from bs4 import BeautifulSoup

from updater.site.abstract_site import AbstractSite
from updater.site.enum import GameVersion


class GitHub(AbstractSite):
    _URLS = [
        'https://www.github.com/',
        'https://github.com/'
    ]

    session = requests.session()

    def __init__(self, url: str):
        super().__init__(url, GameVersion.agnostic)

    def find_zip_url(self):
        return self.url + '/archive/master.zip'

    def get_latest_version(self):
        try:
            response = GitHub.session.get(self.url + '/commits/master')
            response.raise_for_status()
            page = BeautifulSoup(response.text, 'html.parser')
            commits = page.find(attrs={'class': 'repository-content'})
            version = commits.find('a', {'class': ['sha', 'btn']}).get_text(strip=True)
            return version
        except Exception as e:
            raise self.version_error() from e

    def get_addon_name(self):
        addon_name = AbstractSite.get_addon_name(self)
        addon_name = addon_name.split('/')[-1]
        return addon_name
