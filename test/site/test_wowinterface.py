import unittest

from updater.site import wowinterface
from updater.site.enum import GameVersion


class TestWowInterface(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.wowinterface.com/downloads/info11190-Bartender4.html'
        self.wowinterface = wowinterface.WoWInterface(self.url, GameVersion.retail)

    def test_integration_wowinterface_find_zip_url(self):
        zip_url = self.wowinterface.find_zip_url()
        # example: https://cdn.wowinterface.com/downloads/file11190/Bartender4-4.8.3.zip?156152944115
        self.assertRegex(zip_url,
                         r"https:\/\/cdn.wowinterface.com\/downloads\/file[0-9]+"
                         r"\/[a-zA-Z0-9]+-[0-9]+\.[0-9]+\.[0-9]+\.zip\?[0-9]+")

    def test_integration_wowinterface_get_addon_name(self):
        addon_name = self.wowinterface.get_addon_name()
        self.assertEqual(addon_name, 'Bartender4')

    def test_integration_wowinterface_get_latest_version(self):
        latest_version = self.wowinterface.get_latest_version()
        # something like 4.5.6
        self.assertRegex(latest_version, r"[0-9]+\.[0-9]+\.[0-9]+")

    def test_wowinterface_get_supported_urls(self):
        supported_urls = self.wowinterface.get_supported_urls()
        self.assertIsNotNone(supported_urls)
        self.assertTrue(len(supported_urls) != 0)


if __name__ == '__main__':
    unittest.main()
