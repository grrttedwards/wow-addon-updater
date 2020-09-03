import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Generator

import bs4
import cloudscraper

from updater.site import CURSE_UA
from updater.site.abstract_site import AbstractSite, SiteError
from updater.site.enum import AddonVersion, GameVersion

logger = logging.getLogger(__name__)


@dataclass
class CurseAddonVersion:
    type: AddonVersion
    name: str
    size: str
    uploaded: str
    game_version: str
    downloads: int
    download_link: str

    @classmethod
    def from_tr(cls, tr: bs4.element.Tag):
        cells = tr.find_all('td')
        name = cells[1].text.strip()
        size = cells[2].text.strip()
        uploaded = datetime.fromtimestamp(int(cells[3].find('abbr').attrs.get('data-epoch'))).isoformat()
        game_version = cells[4].text.strip()
        downloads = int(cells[5].text.replace(',', '').strip())

        return cls(type=cls.get_type(cells[0]), name=name, size=size,
                   uploaded=uploaded, game_version=game_version, downloads=downloads,
                   download_link=cls.get_link(cells[6]))

    @staticmethod
    def get_type(td: bs4.element.Tag) -> AddonVersion:
        class_fields = td.find('div').attrs.get('class')
        bg_field = next(field for field in class_fields if field.startswith('bg-'))
        if 'blue' in bg_field:
            return AddonVersion.beta
        elif 'green' in bg_field:
            return AddonVersion.release
        elif 'offset' in bg_field:
            return AddonVersion.alpha
        else:
            raise ValueError

    @staticmethod
    def get_link(td: bs4.element.Tag) -> str:
        relative_link = td.find('a').attrs.get('href')
        return f'https://www.curseforge.com{relative_link}/file'


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

    def __init__(self, url: str, game_version: GameVersion, addon_version: AddonVersion = AddonVersion.release):
        url = Curse._convert_old_curse_urls(url)
        super().__init__(url, game_version)
        self.addon_version = addon_version

    def find_zip_url(self):
        try:
            latest_release = next(version for version in self.versions() if version.type >= self.addon_version)
            return latest_release.download_link
        except Exception as e:
            raise self.download_error() from e

    def versions(self, *, page=1) -> Generator[CurseAddonVersion, None, None]:
        """Yields a sequence of CurseAddonVersions corresponding to addon releases

        Ordered descending in time, so the first version yielded is the most recent.
        Will page through until exhausted.
        """
        if self.game_version == GameVersion.classic:
            game_version_filter = '1738749986:67408'
        elif self.game_version == GameVersion.retail:
            game_version_filter = '1738749986:517'
        else:  # Agnostic version
            game_version_filter = ''
        request_params = {'filter-game-version': game_version_filter, 'page': page}
        try:
            p = Curse.session.get(f'{self.url}/files/all', params=request_params)
            soup = bs4.BeautifulSoup(p.text, 'html.parser')
            versions_table = soup.find('table', {'class': 'listing listing-project-file project-file-listing b-table b-table-a'})
            # Header row consumed by _
            _, *version_rows = versions_table.find_all('tr')
            yield from (CurseAddonVersion.from_tr(row) for row in version_rows)

            # determine if there are more pages of versions, recurse if so
            pages_exist = soup.find('div', {'class': 'pagination pagination-top flex items-center'})
            inactive_next_page = soup.find('div', {'class': 'pagination-next h-6 w-6 flex items-center justify-center pagination-next--inactive'})
            if pages_exist and not inactive_next_page:
                yield from self.versions(page=page+1)
        except Exception as e:
            raise self.version_error() from e

    def get_latest_version(self) -> str:
        """Returns the latest version released for retail/classic

        The `version.type >= self.addon_version` logic chooses the most recent
        addon according to the ordering that release > beta > alpha. So if you
        are following the beta track and a new alpha version is release, you won't
        get it, but a new release version you will.

        Returns the name of the most recent release.
        """
        latest_release = next(version for version in self.versions() if version.type >= self.addon_version)
        return latest_release.name

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
