import unittest
from unittest.mock import patch, Mock

from updater.manager import addon_manager
from updater.manager.addon_manager import AddonManager
from updater.site.abstract_site import AbstractSite


class MockSite(AbstractSite):

    @classmethod
    def get_supported_urls(cls) -> [str]:
        return ['url/']

    def find_zip_url(self) -> str:
        return 'url/something/download'

    def get_latest_version(self) -> str:
        return 'latest_version'


TEST_URL = 'url/something'
EXP_NAME = 'something'
EXP_INST_VERSION = 'installed_version'
EXP_LATEST_VERSION = AddonManager._UNAVAILABLE
EXP_MANIFEST = [[EXP_NAME, TEST_URL, EXP_INST_VERSION, EXP_LATEST_VERSION]]


class TestAddonManager(unittest.TestCase):
    def setUp(self):
        self.mock_site = MockSite(TEST_URL)
        patcher = patch('updater.manager.addon_manager.site_handler.get_handler')
        patcher.start().return_value = MockSite(TEST_URL)
        with patch.object(addon_manager.AddonManager, "__init__", lambda x: None):
            self.manager = addon_manager.AddonManager()
        self.manager.manifest = []
        self.manager.get_installed_version = Mock(return_value=EXP_INST_VERSION)

        self.addCleanup(patcher.stop)

    def test_download_fail_doesnt_install_addon(self):
        self.manager.get_addon_zip = Mock(side_effect=Exception())
        self.manager.update_addon(TEST_URL)
        self.assertFailedInstall()

    def test_find_download_url_fail_doesnt_install_addon(self):
        self.mock_site.find_zip_url = Mock(side_effect=Exception())
        self.manager.update_addon(TEST_URL)
        self.assertFailedInstall()

    def test_get_latest_version_fail_doesnt_install_addon(self):
        self.mock_site.get_latest_version = Mock(side_effect=Exception())
        self.manager.update_addon(TEST_URL)
        self.assertFailedInstall()

    def assertFailedInstall(self):
        self.assertListEqual([[EXP_NAME, TEST_URL, EXP_INST_VERSION, EXP_LATEST_VERSION]],
                             self.manager.manifest)


if __name__ == '__main__':
    unittest.main()
