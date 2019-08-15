from updater.site.abstract_site import AbstractSite
from updater.site.curse import Curse
from updater.site.tukui import Tukui
from updater.site.wowace import WoWAce
from updater.site.wowinterface import WoWInterface


class UnknownSiteError(RuntimeError):
    pass


def get_handler(url: str) -> AbstractSite:
    if Curse.handles(url):
        return Curse(url)
    elif WoWAce.handles(url):
        return WoWAce(url)
    elif Tukui.handles(url):
        return Tukui(url)
    elif WoWInterface.handles(url):
        return WoWInterface(url)

    # for subclass in Site.__subclasses__():
    #     if subclass.handles(url):
    #         return subclass(url)
    else:
        # Unknown site
        raise UnknownSiteError(f"Unknown addon source: {url}")
