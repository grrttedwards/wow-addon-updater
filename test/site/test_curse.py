import unittest

from updater.site import Curse


class TestCurse(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.curseforge.com/wow/addons/bartender4'
        self.curse = Curse.Curse(self.url)

    def test_integration_curse_find_zip_url(self):
        zip_url = self.curse.find_zip_url()
        # example: https://www.curseforge.com/wow/addons/bartender4/download/2730531/file
        self.assertRegex(zip_url, rf"{self.url}/download/[0-9]+/file")

    def test_integration_curse_get_addon_name(self):
        addon_name = self.curse.get_addon_name()
        self.assertEqual(addon_name, 'bartender4')

    def test_integration_curse_get_latest_version(self):
        latest_version = self.curse.get_latest_version()
        # something like 4.5.6
        self.assertRegex(latest_version, r"[0-9]+\.[0-9]+\.[0-9]+")

    def test_curse_get_supported_urls(self):
        supported_urls = self.curse.get_supported_urls()
        self.assertIsNotNone(supported_urls)
        self.assertTrue(len(supported_urls) != 0)


if __name__ == '__main__':
    unittest.main()
