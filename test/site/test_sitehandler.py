import unittest
from unittest.mock import MagicMock

from updater.site import SiteHandler, Curse, WoWAce, WoWInterface, Tukui


class TestSiteHandler(unittest.TestCase):
    def test_handles_curse(self):
        for url in Curse.Curse.get_supported_urls():
            Curse.convert_old_curse_urls = MagicMock(return_value=url)
            handler = SiteHandler.get_handler(url)
            self.assertIsInstance(handler, Curse.Curse)

    def test_handles_wowace(self):
        for url in WoWAce.WoWAce.get_supported_urls():
            handler = SiteHandler.get_handler(url)
            self.assertIsInstance(handler, WoWAce.WoWAce)

    def test_handles_tukui(self):
        for url in WoWInterface.WoWInterface.get_supported_urls():
            handler = SiteHandler.get_handler(url)
            self.assertIsInstance(handler, WoWInterface.WoWInterface)

    def test_handles_wowinterface(self):
        for url in Tukui.Tukui.get_supported_urls():
            handler = SiteHandler.get_handler(url)
            self.assertIsInstance(handler, Tukui.Tukui)


if __name__ == '__main__':
    unittest.main()
