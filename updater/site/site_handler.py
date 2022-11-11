from updater.site.abstract_site import AbstractSite
from updater.site.curse import Curse
from updater.site.enum import AddonVersion, GameVersion
from updater.site.github import GitHub
from updater.site.github_release import GitHubRelease
from updater.site.tukui import Tukui
from updater.site.wowace import WoWAce
from updater.site.wowinterface import WoWInterface


class UnknownSiteError(RuntimeError):
    pass


def get_handler(url: str, game_version: GameVersion,
                addon_version: AddonVersion = AddonVersion.release) -> AbstractSite:
    if Curse.handles(url):
        return Curse(url, game_version, addon_version)
    elif WoWAce.handles(url):
        return WoWAce(url, game_version)
    elif Tukui.handles(url):
        return Tukui(url)
    elif WoWInterface.handles(url):
        return WoWInterface(url, game_version)
    elif GitHub.handles(url):
        return GitHub(url)
    elif GitHubRelease.handles(url):
        return GitHubRelease(url)

    # for subclass in Site.__subclasses__():
    #     if subclass.handles(url):
    #         return subclass(url)
    else:
        # Unknown site
        raise UnknownSiteError(f"Unknown addon source: {url}")
