import logging
import re

import cloudscraper

from updater.site import CURSE_UA
from updater.site.abstract_site import AbstractSite, SiteError
from updater.site.enum import GameVersion

logger = logging.getLogger(__name__)


class Curse(AbstractSite):
    _OLD_URL = 'https://mods.curse.com/addons/wow/'
    _OLD_PROJECT_URL = 'https://wow.curseforge.com/projects/'

    _URLS = [
        'https://www.curseforge.com/wow/addons/',
        'https://curseforge.com/wow/addons/',
        _OLD_URL,
        _OLD_PROJECT_URL
    ]

    session = cloudscraper.create_scraper(browser=CURSE_UA)

    def __init__(self, url: str, game_version: GameVersion):
        url = Curse._convert_old_curse_urls(url)
        super().__init__(url, game_version)

    def find_zip_url(self):
        try:
            page = Curse.session.get(self.url)
            page.raise_for_status()  # Raise an exception for HTTP errors
            content_string = str(page.content)
            main_zip_url, *classic_zip_url = re.findall(
                r"cf-recentfiles-credits-wrapper ml-auto my-auto.+?href=\"(?P<download>.+?)\"",
                content_string)
            # if classic, choose the explicit "classic download" listed, or fall back to the only download available
            zip_url = classic_zip_url[-1] if self.game_version is GameVersion.classic and classic_zip_url else main_zip_url
            return f'https://www.curseforge.com{zip_url}/file'
        except Exception as e:
            raise self.download_error() from e

    def get_latest_version(self):
        try:
            page = Curse.session.get(self.url)
            if page.status_code in [403, 503]:
                logger.error("Curse is blocking requests because it thinks you are a bot... please try later.")
            page.raise_for_status()  # Raise an exception for HTTP errors
            content_string = str(page.content)
            # the first one encountered will be the WoW retail version
            main_version, *classic_version = re.findall(
                r"cf-recentfiles.+?data-id=.+?data-name=\"(?P<version>.+?)\"",
                content_string)
            # if classic, choose the explicit "classic version" listed, or fall back to the only version available
            return classic_version[-1] if self.game_version is GameVersion.classic and classic_version else main_version
        except Exception as e:
            raise self.version_error() from e

    @classmethod
    def _convert_old_curse_urls(cls, url: str) -> str:
        if any(old_url in url for old_url in [Curse._OLD_URL, Curse._OLD_PROJECT_URL]):
            try:
                # Some old URL's may point to nonexistent pages. Rather than guess at what the new
                # name and URL is, just try to load the old URL and see where Curse redirects us to.
                page = Curse.session.get(url)
                page.raise_for_status()
                return page.url
            except Exception as e:
                raise SiteError(f"Failed to find the current page for old URL: {url}") from e
        else:
            return url
