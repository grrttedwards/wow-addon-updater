import unittest
from dataclasses import dataclass
from typing import Collection
from unittest.mock import MagicMock, patch

from updater.site import curse
from updater.site.enum import AddonVersion, GameVersion
from test.testutils import get_file


@dataclass
class VersionTestData:
    url: str
    version_regex: str
    supported_game_versions: Collection[GameVersion]


ALL_VERSIONS = (GameVersion.classic, GameVersion.retail, GameVersion.agnostic,GameVersion.tbc,GameVersion.wrath)

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

url_redirect_test_data = VersionTestData(url='https://www.curseforge.com/wow/addons/method-dungeon-tools',
                                         version_regex=r'v[0-9]+\.[0-9]+\.[0-9]+',
                                         supported_game_versions=(GameVersion.retail, GameVersion.agnostic))

MOCK_VERSION_PAGE = MagicMock()
with open(get_file('mock-curse-version-addons-simc.html'), 'r') as f:
    MOCK_VERSION_PAGE.text = f.read()


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

    def test_curse_unsupported_game_version(self):
        # classiccodex should throw an version error when searching for an
        # unsupported retail game version
        classiccodex = version_test_data[0]
        c = curse.Curse(classiccodex.url, GameVersion.retail)
        self.assertRaises(curse.SiteError, c.get_latest_version)

    @patch.object(curse.Curse.session, 'get', MagicMock(return_value=MOCK_VERSION_PAGE))
    def test_curse_versions_parsing(self):
        # The curse object is a throwaway here
        _ = version_test_data[1]
        d = curse.Curse(_.url, GameVersion.retail, AddonVersion.release)
        # This mock pulls a static example of a curse addon files page for testing
        expected_results = [
            (AddonVersion.release, 'v1.12.5'),
            (AddonVersion.beta, 'v1.12.0-beta-2'),
            (AddonVersion.alpha, 'v9.0.1-alpha-8')
        ]
        for addon_version, expected_value in expected_results:
            with self.subTest((addon_version, expected_value)):
                d.addon_version = addon_version
                self.assertEqual(d.get_latest_version(), expected_value)

    def test_curse_url_redirect(self):
        test_data = url_redirect_test_data
        for game_version in test_data.supported_game_versions:
            with self.subTest((game_version, test_data.url, test_data.version_regex)):
                c = curse.Curse(test_data.url, game_version)
                latest_version = c.get_latest_version()
                self.assertRegex(latest_version, test_data.version_regex)


if __name__ == '__main__':
    unittest.main()
