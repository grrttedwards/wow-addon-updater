import re

import requests

from updater.site.abstract_site import AbstractSite
from updater.site.enum import GameVersion


class WoWAce(AbstractSite):
    _URL = 'https://www.wowace.com/projects/'

    def __init__(self, url: str, game_version: GameVersion):
        if game_version != GameVersion.retail:
            raise NotImplementedError("Updating classic addons are not yet supported for WoWAce.")
        super().__init__(url, game_version)

    @classmethod
    def get_supported_urls(cls):
        return [cls._URL]

    def find_zip_url(self):
        return self.url + '/files/latest'

    def get_latest_version(self):
        try:
            page = requests.get(self.url + '/files')
            if page.status_code in [403, 503]:
                print("WoWAce (Curse) is temporarily blocking requests because it thinks you are a bot... please try later. "
                      "Consider finding this addon on WoWInterface or GitHub.")
            page.raise_for_status()  # Raise an exception for HTTP errors
            content_string = str(page.content)
            # the first one encountered will be the WoW retail version
            version = re.search(
                r"project-file-name-container.+?data-id=.+?data-name=\"(?P<version>.+?)\"",
                content_string).group('version')
            return version
        except Exception as e:
            raise self.version_error() from e
