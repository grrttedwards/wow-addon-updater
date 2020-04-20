import requests
from bs4 import BeautifulSoup

from updater.site.abstract_site import AbstractSite
from updater.site.enum import GameVersion


class Tukui(AbstractSite):
    _URLS = [
        'https://www.tukui.org/'
    ]

    session = requests.session()

    latest_version = None

    def __init__(self, url: str):
        super().__init__(url, GameVersion.agnostic)

    def find_zip_url(self):
        version = self.get_latest_version()
        
        # like https://www.tukui.org/classic-addons.php?download=2
        downloadpage = self.url.replace('id', 'download')
        return downloadpage          

    def get_latest_version(self):
        if self.latest_version:
            return self.latest_version
        try:
            response = Tukui.session.get(self.url + '#extras')
            response.raise_for_status()
            content_string = str(response.content)
            index_of_ver = content_string.find('The latest version of this addon is <b class="VIP">') + 51
            end_tag = content_string.find('</b>')
            return content_string[index_of_ver:end_tag].strip()
        except Exception as e:
            raise self.version_error() from e

    def get_addon_name(self):
        response = Tukui.session.get(self.url)
        response.raise_for_status()
        page = BeautifulSoup(response.text, 'html.parser')
        name = page.find('span', attrs={'class': 'Member'})
        addon_name = name.text.strip()
        return addon_name