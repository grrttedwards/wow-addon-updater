import unittest

from updater.site import curse

version_test_data = [
    ['https://www.curseforge.com/wow/addons/bartender4', 'bartender4', r"[0-9]+\.[0-9]+\.[0-9]+"],
    ['https://www.curseforge.com/wow/addons/big-wigs', 'big-wigs', r"v[0-9]+"],
    ['https://www.curseforge.com/wow/addons/deadly-boss-mods', 'deadly-boss-mods', r"[0-9]+\.[0-9]+\.[0-9]+"],
    ['https://www.curseforge.com/wow/addons/weakauras-2', 'weakauras-2', r"[0-9]+\.[0-9]+\.[0-9]+"]
]


class TestCurse(unittest.TestCase):
    def setUp(self):
        self.url = 'https://www.curseforge.com/wow/addons/bartender4'
        self.curse = curse.Curse(self.url)

    def test_integration_curse_find_zip_url(self):
        zip_url = self.curse.find_zip_url()
        # example: https://www.curseforge.com/wow/addons/bartender4/download/2730531/file
        self.assertRegex(zip_url, rf"{self.url}/download/[0-9]+/file")

    def test_integration_curse_get_addon_name(self):
        addon_name = self.curse.get_addon_name()
        self.assertEqual(addon_name, 'bartender4')

    def test_integration_curse_get_latest_version(self):
        for data in version_test_data:
            url, name, version_regex = data
            thiscurse = curse.Curse(url)
            latest_version = thiscurse.get_latest_version()
            with self.subTest(data):
                # something like 4.5.6, or v163
                self.assertRegex(latest_version, version_regex)

    def test_curse_get_supported_urls(self):
        supported_urls = self.curse.get_supported_urls()
        self.assertIsNotNone(supported_urls)
        self.assertTrue(len(supported_urls) != 0)


if __name__ == '__main__':
    unittest.main()
