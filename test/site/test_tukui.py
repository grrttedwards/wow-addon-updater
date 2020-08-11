import unittest

from updater.site.tukui import Tukui

version_test_data = [
    ['https://www.tukui.org/classic-addons.php?id=1', 'https://www.tukui.org/classic-addons.php?download=1', 'Tukui'],
    ['https://www.tukui.org/classic-addons.php?id=2', 'https://www.tukui.org/classic-addons.php?download=2', 'ElvUI'],
    ['https://www.tukui.org/download.php?ui=tukui', 'https://www.tukui.org/downloads/tukui-', 'Tukui'],
    ['https://www.tukui.org/download.php?ui=elvui', 'https://www.tukui.org/downloads/elvui-', 'ElvUI'],
    ['https://www.tukui.org/addons.php?id=3', 'https://www.tukui.org/addons.php?download=3', 'AddOnSkins']
]


class TestTukui(unittest.TestCase):
    def data(self):
        for url, exp_dl_url, exp_name in version_test_data:
            with self.subTest((url, exp_dl_url, exp_name)):
                yield Tukui(url), exp_dl_url, exp_name

    def test_integration_tukui_find_zip_url(self):
        for client, exp_dl_url, exp_name in self.data():
            zip_url = client.find_zip_url()
            self.assertTrue(exp_dl_url in zip_url)

    def test_integration_tukui_get_addon_name(self):
        for client, exp_dl_url, exp_name in self.data():
            addon_name = client.get_addon_name()
            self.assertEqual(addon_name, exp_name)

    def test_integration_tukui_get_latest_version(self):
        for client, exp_dl_url, exp_name in self.data():
            latest_version = client.get_latest_version()
            self.assertRegex(latest_version, r'([0-9]+\.[0-9]+)')  # something like v12.34

    def test_tukui_get_supported_urls(self):
        for client, exp_dl_url, exp_name in self.data():
            supported_urls = client.get_supported_urls()
            self.assertIsNotNone(supported_urls)
            self.assertTrue(len(supported_urls) != 0)


if __name__ == '__main__':
    unittest.main()
