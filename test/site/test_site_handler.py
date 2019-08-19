import unittest
from unittest.mock import MagicMock

from updater.site import site_handler
from updater.site.curse import Curse
from updater.site.enum import GameVersion
from updater.site.tukui import Tukui
from updater.site.wowace import WoWAce
from updater.site.wowinterface import WoWInterface


class TestSiteHandler(unittest.TestCase):
    def test_handles_curse(self):
        for url in Curse.get_supported_urls():
            Curse._convert_old_curse_urls = MagicMock(return_value=url)
            handler = site_handler.get_handler(url, GameVersion.retail)
            self.assertIsInstance(handler, Curse)

    def test_handles_wowace(self):
        for url in WoWAce.get_supported_urls():
            handler = site_handler.get_handler(url, GameVersion.retail)
            self.assertIsInstance(handler, WoWAce)

    def test_handles_tukui(self):
        for url in WoWInterface.get_supported_urls():
            handler = site_handler.get_handler(url, GameVersion.retail)
            self.assertIsInstance(handler, WoWInterface)

    def test_handles_wowinterface(self):
        for url in Tukui.get_supported_urls():
            handler = site_handler.get_handler(url, GameVersion.retail)
            self.assertIsInstance(handler, Tukui)


if __name__ == '__main__':
    unittest.main()
