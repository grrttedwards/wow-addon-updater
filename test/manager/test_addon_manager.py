import os
import tempfile
import unittest
import zipfile
from unittest.mock import patch, Mock

from test import testutils
from updater.manager import addon_manager
from updater.manager.addon_manager import AddonManager
from updater.site import curse, github
from updater.site.abstract_site import AbstractSite, SiteError
from updater.site.enum import GameVersion


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
        self.mock_site = MockSite(TEST_URL, GameVersion.agnostic)
        patcher = patch('updater.manager.addon_manager.site_handler.get_handler')
        patcher.start().return_value = self.mock_site
        with patch.object(addon_manager.AddonManager, "__init__", lambda x, y: None):
            self.manager = addon_manager.AddonManager('config.ini')
        self.manager.manifest = []
        self.manager.get_installed_version = Mock(return_value=EXP_INST_VERSION)
        self.manager.game_version = GameVersion.retail

        self.addCleanup(patcher.stop)

    def assertFailedInstall(self):
        self.assertListEqual([[EXP_NAME, TEST_URL, EXP_INST_VERSION, EXP_LATEST_VERSION]],
                             self.manager.manifest)

    def extractAddon(self, filename, temp_dir, site, subfolder=None):
        self.manager.wow_addon_location = temp_dir
        mock_zipfile = zipfile.ZipFile(testutils.get_file(filename))
        self.manager.extract_to_addons(mock_zipfile, subfolder, site)

    def assertExtractionSuccess(self, temp_dir, *args):
        for index in range(1, len(args)):
            sub_args = args[:index]
            if index == len(args):
                # the last one should be a file, not directory
                self.assertTrue(os.path.isfile(os.path.join(temp_dir, *sub_args)))
            else:
                self.assertTrue(os.path.isdir(os.path.join(temp_dir, *sub_args)))

    def test_download_fail_doesnt_install_addon(self):
        self.manager.get_addon_zip = Mock(side_effect=Exception())
        self.manager.update_addon(TEST_URL)
        self.assertFailedInstall()

    def test_find_download_url_fail_doesnt_install_addon(self):
        self.mock_site.find_zip_url = Mock(side_effect=Exception())
        self.manager.update_addon(TEST_URL)
        self.assertFailedInstall()

    def test_get_latest_version_fail_doesnt_install_addon(self):
        self.mock_site.get_latest_version = Mock(side_effect=SiteError())
        self.manager.update_addon(TEST_URL)
        self.assertFailedInstall()

    """ 
    Issue #80 https://github.com/grrttedwards/wow-addon-updater/issues/80
    """
    def test_subfolder_extraction_fail_doesnt_install_addon(self):
        self.manager.extract_to_addons = Mock(side_effect=KeyError())
        self.manager.update_addon(TEST_URL)
        self.assertFailedInstall()

    def test_extract_archive_subfolder(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.extractAddon('some-fake-addon-with-many-folders.zip', temp_dir, curse.Curse("", GameVersion.retail),
                              subfolder='FolderA')
            self.assertExtractionSuccess(temp_dir, 'FolderA', 'sub-folder', 'file1.txt')

    def test_extract_archive_subfolder_git(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.extractAddon('some-fake-addon-master.zip', temp_dir, github.GitHub(""),
                              subfolder='sub-folder')
            self.assertExtractionSuccess(temp_dir, 'sub-folder', 'file1.txt')

    def test_extract_entire_archive(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.extractAddon('some-fake-addon.zip', temp_dir, curse.Curse("", GameVersion.retail))
            self.assertExtractionSuccess(temp_dir, 'some-fake-addon', 'sub-folder', 'file1.txt')

    def test_extract_entire_archive_github_master_zipball(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.extractAddon('some-fake-addon-master.zip', temp_dir, github.GitHub(""))
            self.assertExtractionSuccess(temp_dir, 'some-fake-addon', 'sub-folder', 'file1.txt')

    def test_extract_entire_archive_curse(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.extractAddon('some-fake-addon-from-curse.zip', temp_dir, curse.Curse("", GameVersion.retail))
            self.assertExtractionSuccess(temp_dir, 'AddonName', 'sub-folder', 'file1.txt')

    def test_extract_archive_with_multiple_folders(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            self.extractAddon('some-fake-addon-with-many-folders.zip', temp_dir, curse.Curse("", GameVersion.retail))
            self.assertExtractionSuccess(temp_dir, 'FolderA', 'sub-folder', 'file1.txt')
            self.assertExtractionSuccess(temp_dir, 'FolderB', 'fileB.txt')
            self.assertExtractionSuccess(temp_dir, 'FolderC', 'fileC.txt')

    """ 
    Issue #80 https://github.com/grrttedwards/wow-addon-updater/issues/80
    """
    def test_zip_subfolder_extract_fail_raises_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            def extract_should_fail():
                return self.extractAddon('some-fake-addon.zip', temp_dir, None, subfolder='existing-addon')
            existing_addon_dir = os.path.join(temp_dir, 'existing-addon')
            os.mkdir(existing_addon_dir)
            self.assertRaises(KeyError, extract_should_fail)
            self.assertTrue(os.path.isdir(existing_addon_dir))


if __name__ == '__main__':
    unittest.main()
