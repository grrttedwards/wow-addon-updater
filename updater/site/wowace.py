from bs4 import BeautifulSoup

from updater.site.abstract_site import AbstractSite
from updater.site.enum import GameVersion


class WoWAce(AbstractSite):
    _URLS = [
        'https://www.wowace.com/projects/',
        'https://wowace.com/projects/'
    ]

    session = AbstractSite.get_scraper()

    def __init__(self, url: str, game_version: GameVersion):
        super().__init__(url, game_version)
        self._page = None
        self._latest_version = None

    def find_zip_url(self):
        return f"https://www.wowace.com{self.get_page().find('a', text=self.get_latest_version()).get('href')}/download"

    def get_latest_version(self):
        if self._latest_version:
            return self._latest_version

        try:
            page = self.get_page()
            recent_wrappers = page.find_all('ul', {'class': 'cf-recentfiles'})

            if (len(recent_wrappers) == 1) or (self.game_version == GameVersion.retail):
                version = recent_wrappers[0].find(
                    'a', {'data-action': 'file-link'}).text
            else:
                version = recent_wrappers[1].find(
                    'a', {'data-action': 'file-link'}).text

            self._latest_version = version
            return version
        except Exception as e:
            raise self.version_error() from e

    def get_page(self):
        if self._page:
            return self._page
        try:
            page = WoWAce.session.get(self.url)
            if page.status_code in [403, 503]:
                print(
                    'WoWAce (Curse) is blocking requests because it thinks you are a bot... please try later.')
            page.raise_for_status()  # Raise an exception for HTTP errors
            self._page = BeautifulSoup(page.text, 'html.parser')
            return self._page
        except Exception as e:
            raise self.version_error() from e
