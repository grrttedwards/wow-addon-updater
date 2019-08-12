import unittest
from unittest.mock import MagicMock

from updater.site import SiteHandler
from updater.site.Curse import Curse
from updater.site.WoWAce import WoWAce
from updater.site.Tukui import Tukui
from updater.site.WoWInterface import WoWInterface


class TestSiteHandler(unittest.TestCase):
    def test_handles_curse(self):
        for url in Curse.get_supported_urls():
            Curse._convert_old_curse_urls = MagicMock(return_value=url)
            handler = SiteHandler.get_handler(url)
            self.assertIsInstance(handler, Curse)

    def test_handles_wowace(self):
        for url in WoWAce.get_supported_urls():
            handler = SiteHandler.get_handler(url)
            self.assertIsInstance(handler, WoWAce)

    def test_handles_tukui(self):
        for url in WoWInterface.get_supported_urls():
            handler = SiteHandler.get_handler(url)
            self.assertIsInstance(handler, WoWInterface)

    def test_handles_wowinterface(self):
        for url in Tukui.get_supported_urls():
            handler = SiteHandler.get_handler(url)
            self.assertIsInstance(handler, Tukui)


if __name__ == '__main__':
    unittest.main()
