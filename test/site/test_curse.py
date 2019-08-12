import unittest

from updater.site import Curse


@unittest.SkipTest
class TestCurse(unittest.TestCase):
    def setUp(self):
        self.curse = Curse.Curse("")

    # todo
    def test_integration_curse_find_zip_url(self):
        # self.curse.find_zip_url()
        self.assertTrue(False)

    # todo
    def test_integration_curse_get_addon_name(self):
        # self.curse.get_addon_name()
        self.assertTrue(False)

    # todo
    def test_integration_curse_get_latest_version(self):
        # self.curse.get_latest_version()
        self.assertTrue(False)

    # todo
    def test_integration_curse_get_supported_urls(self):
        # self.curse.get_supported_urls()
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
