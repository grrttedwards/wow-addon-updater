import unittest
from dataclasses import dataclass
from typing import Collection

from updater.site import curse
from updater.site.enum import GameVersion


@dataclass
class VersionTestData:
    url: str
    version_regex: str
    supported_game_versions: Collection[GameVersion]


ALL_VERSIONS = (GameVersion.classic, GameVersion.retail, GameVersion.agnostic)

version_test_data = [
    VersionTestData(url='https://www.curseforge.com/wow/addons/classiccodex',
                    version_regex=r'[0-9]+\.[0-9]+\.[0-9]+',
                    supported_game_versions=(GameVersion.classic, GameVersion.agnostic)),
    VersionTestData(url='https://www.curseforge.com/wow/addons/bartender4',
                    version_regex=r"[0-9]+\.[0-9]+\.[0-9]+",
                    supported_game_versions=ALL_VERSIONS),
    VersionTestData(url='https://www.curseforge.com/wow/addons/big-wigs',
                    version_regex=r"v[0-9]+",
                    supported_game_versions=ALL_VERSIONS),
    VersionTestData(url='https://www.curseforge.com/wow/addons/deadly-boss-mods',
                    version_regex=r"[0-9]+\.[0-9]+\.[0-9]+",
                    supported_game_versions=ALL_VERSIONS),
    VersionTestData(url='https://www.curseforge.com/wow/addons/weakauras-2',
                    version_regex=r"[0-9]+\.[0-9]+\.[0-9]+",
                    supported_game_versions=ALL_VERSIONS)
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
        for vtd in version_test_data:
            for game_version in vtd.supported_game_versions:
                with self.subTest((game_version, vtd.url, vtd.version_regex)):
                    c = curse.Curse(vtd.url, game_version)
                    latest_version = c.get_latest_version()
                    # something like 4.5.6, or v163
                    self.assertRegex(latest_version, vtd.version_regex)

    def test_curse_get_supported_urls(self):
        supported_urls = self.curse.get_supported_urls()
        self.assertIsNotNone(supported_urls)
        self.assertTrue(len(supported_urls) != 0)


if __name__ == '__main__':
    unittest.main()
