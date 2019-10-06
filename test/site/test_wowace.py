import unittest

from updater.site import wowace
from updater.site.enum import GameVersion

version_test_data = [
    ['https://www.wowace.com/projects/prat-3-0', r'[0-9]+\.[0-9]+\.[0-9]+'],
    ['https://www.wowace.com/projects/bartender4', r'[0-9]+\.[0-9]+\.[0-9]+'],
    ['https://www.wowace.com/projects/shadowed-unit-frames', r'v[0-9]+'],
    ['https://www.wowace.com/projects/acp', r'[0-9]+\.[0-9]+\.[0-9]+'],
    ['https://www.wowace.com/projects/weakauras-2', r'[0-9]+\.[0-9]+\.[0-9]+']
]

class TestWowAce(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.wowace.com/projects/bartender4'
        self.wowace = wowace.WoWAce(self.url, GameVersion.retail)

    def test_integration_wowace_find_zip_url(self):
        for game_version in GameVersion.__members__.values():
            with self.subTest(game_version):
                c = wowace.WoWAce(self.url, game_version)
                zip_url = c.find_zip_url()
                # example for bartender 4.8.8 release: https://www.wowace.com/projects/bartender4/files/2794704/download
                self.assertRegex(zip_url.lower(), rf'{self.url}/files/[0-9]+/download')

    def test_integration_wowace_get_addon_name(self):
        addon_name = self.wowace.get_addon_name()
        self.assertEqual(addon_name, 'bartender4')

    def test_integration_wowace_get_latest_version(self):
        for url, version_regex in version_test_data:
            for game_version in GameVersion.__members__.values():
                with self.subTest((game_version, url, version_regex)):
                    c = wowace.WoWAce(url, game_version)
                    latest_version = c.get_latest_version()
                    # something like 4.5.6, or v163
                    self.assertRegex(latest_version, version_regex)

    def test_wowace_get_supported_urls(self):
        supported_urls = self.wowace.get_supported_urls()
        self.assertIsNotNone(supported_urls)
        self.assertTrue(len(supported_urls) != 0)


if __name__ == '__main__':
    unittest.main()
