import unittest

from updater.site.github import Github


class TestGithub(unittest.TestCase):
    def setUp(self):
        self.url = 'https://github.com/smp4903/FiveSecondRule'
        self.github = Github(self.url)

    def test_integration_tukui_find_zip_url(self):
        zip_url = self.github.find_zip_url()
        self.assertEqual(zip_url, f"https://github.com/smp4903/FiveSecondRule/archive/master.zip")

    def test_integration_tukui_get_addon_name(self):
        addon_name = self.github.get_addon_name()
        self.assertEqual(addon_name, 'FiveSecondRule')

    def test_integration_tukui_get_latest_version(self):
        latest_version = self.github.get_latest_version()
        self.assertRegex(latest_version, r"([a-f0-9]{40})")  # something like a SHA-1 hash

    def test_tukui_get_supported_urls(self):
        supported_urls = self.github.get_supported_urls()
        self.assertIsNotNone(supported_urls)
        self.assertTrue(len(supported_urls) != 0)


if __name__ == '__main__':
    unittest.main()
