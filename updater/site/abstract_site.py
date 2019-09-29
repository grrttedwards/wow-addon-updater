from abc import ABC, abstractmethod

import requests

from updater.site.enum import GameVersion


class SiteError(Exception):
    pass


class AbstractSite(ABC):
    # each implementation should declare a static _URLS list of
    _URLS: [str] = None
    # each implementation should create a static session for itself
    session: requests.Session = None

    def __init__(self, url: str, game_version: GameVersion):
        self.url = url
        self.game_version = game_version

    @classmethod
    def handles(cls, url: str) -> bool:
        return any(supported_url in url for supported_url in cls.get_supported_urls())

    @classmethod
    def get_supported_urls(cls) -> [str]:
        if not cls._URLS:
            raise NotImplementedError(f"Can't instantiate class {cls.__name__}"
                                      " without list of supported URLs cls._URLS")
        return cls._URLS

    @abstractmethod
    def find_zip_url(self) -> str:
        pass

    @abstractmethod
    def get_latest_version(self) -> str:
        pass

    def get_addon_name(self) -> str:
        name = self.url
        for url in self.get_supported_urls():
            name = name.replace(url, '')
        return name

    def download_error(self) -> SiteError:
        return SiteError(f"Failed to find downloadable file for game version: {self.game_version}, {self.url}")

    def version_error(self) -> SiteError:
        return SiteError(f"Failed to find addon version number for game version: {self.game_version}, {self.url}")
