import unittest

from updater.site import wowace


class TestWowAce(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.wowace.com/projects/bartender4'
        self.wowace = wowace.WoWAce(self.url)

    def test_integration_wowace_find_zip_url(self):
        zip_url = self.wowace.find_zip_url()
        # example: https://www.wowace.com/projects/bartender4/files/latest
        self.assertEqual(zip_url, f"{self.url}/files/latest")

    def test_integration_wowace_get_addon_name(self):
        addon_name = self.wowace.get_addon_name()
        self.assertEqual(addon_name, 'bartender4')

    def test_integration_wowace_get_latest_version(self):
        latest_version = self.wowace.get_latest_version()
        # something like 4.5.6-1-g1234567
        self.assertRegex(latest_version, r"[0-9]+\.[0-9]+\.[0-9]+")

    def test_wowace_get_supported_urls(self):
        supported_urls = self.wowace.get_supported_urls()
        self.assertIsNotNone(supported_urls)
        self.assertTrue(len(supported_urls) != 0)


if __name__ == '__main__':
    unittest.main()
