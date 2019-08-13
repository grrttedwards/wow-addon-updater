import unittest

from updater.site import Tukui


class TestTukui(unittest.TestCase):
    def setUp(self):
        self.url = 'https://git.tukui.org/elvui/elvui'
        self.tukui = Tukui.Tukui(self.url)

    def test_integration_tukui_find_zip_url(self):
        zip_url = self.tukui.find_zip_url()
        self.assertEqual(zip_url, f"{self.url}/-/archive/master/elvui-master.zip")

    def test_integration_tukui_get_addon_name(self):
        addon_name = self.tukui.get_addon_name()
        self.assertEqual(addon_name, 'elvui')

    def test_integration_tukui_get_latest_version(self):
        latest_version = self.tukui.get_latest_version()
        self.assertRegex(latest_version, r"([a-f0-9]{40})")  # something like a SHA-1 hash

    def test_tukui_get_supported_urls(self):
        supported_urls = self.tukui.get_supported_urls()
        self.assertIsNotNone(supported_urls)
        self.assertTrue(len(supported_urls) != 0)


if __name__ == '__main__':
    unittest.main()
