import logging

import cloudscraper
from bs4 import BeautifulSoup

from updater.site import CURSE_UA
from updater.site.abstract_site import AbstractSite
from updater.site.enum import GameVersion

logger = logging.getLogger(__name__)


class WoWAce(AbstractSite):
    _URLS = [
        'https://www.wowace.com/projects/',
        'https://wowace.com/projects/'
    ]

    session = cloudscraper.create_scraper(browser=CURSE_UA)
    latest_version = None
    page = None

    def __init__(self, url: str, game_version: GameVersion):
        super().__init__(url, game_version)

    def find_zip_url(self):
        return f"https://www.wowace.com{self._get_page().find('a', text=self.get_latest_version()).get('href')}/download"

    def get_latest_version(self):
        if self.latest_version:
            return self.latest_version

        try:
            page = self._get_page()
            recent_wrappers = page.find_all('ul', {'class': 'cf-recentfiles'})

            if (len(recent_wrappers) == 1) or (self.game_version == GameVersion.retail):
                version = recent_wrappers[0].find('a', {'data-action': 'file-link'}).text
            else:
                version = recent_wrappers[1].find('a', {'data-action': 'file-link'}).text

            self.latest_version = version
            return version
        except Exception as e:
            raise self.version_error() from e

    def _get_page(self):
        if self.page:
            return self.page
        try:
            page = WoWAce.session.get(self.url)
            if page.status_code in [403, 503]:
                logger.error('WoWAce (Curse) is blocking requests because it thinks you are a bot... please try later.')
            page.raise_for_status()  # Raise an exception for HTTP errors
            self.page = BeautifulSoup(page.text, 'html.parser')
            return self.page
        except Exception as e:
            raise self.version_error() from e
