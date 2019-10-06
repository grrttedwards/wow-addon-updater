import unittest

from updater.site import curse
from updater.site.enum import GameVersion

version_test_data = [
    ['https://www.curseforge.com/wow/addons/classiccodex', r'[0-9]+\.[0-9]+\.[0-9]+'],
    ['https://www.curseforge.com/wow/addons/bartender4', r"[0-9]+\.[0-9]+\.[0-9]+"],
    ['https://www.curseforge.com/wow/addons/big-wigs', r"v[0-9]+"],
    ['https://www.curseforge.com/wow/addons/deadly-boss-mods', r"[0-9]+\.[0-9]+\.[0-9]+"],
    ['https://www.curseforge.com/wow/addons/weakauras-2', r"[0-9]+\.[0-9]+\.[0-9]+"]
]


class TestCurse(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.curseforge.com/wow/addons/bartender4'
        self.curse = curse.Curse(self.url, GameVersion.retail)

    def test_integration_curse_find_zip_url(self):
        for game_version in GameVersion.__members__.values():
            with self.subTest(game_version):
                c = curse.Curse(self.url, game_version)
                zip_url = c.find_zip_url()
                # example: https://www.curseforge.com/wow/addons/bartender4/download/2730531/file
                self.assertRegex(zip_url.lower(), rf"{self.url}/download/[0-9]+/file")

    def test_integration_curse_get_addon_name(self):
        addon_name = self.curse.get_addon_name()
        self.assertEqual(addon_name, 'bartender4')

    def test_integration_curse_get_latest_version(self):
        for url, version_regex in version_test_data:
            for game_version in GameVersion.__members__.values():
                with self.subTest((game_version, url, version_regex)):
                    c = curse.Curse(url, game_version)
                    latest_version = c.get_latest_version()
                    # something like 4.5.6, or v163
                    self.assertRegex(latest_version, version_regex)

    def test_curse_get_supported_urls(self):
        supported_urls = self.curse.get_supported_urls()
        self.assertIsNotNone(supported_urls)
        self.assertTrue(len(supported_urls) != 0)


if __name__ == '__main__':
    unittest.main()
