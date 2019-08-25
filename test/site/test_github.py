import unittest

from updater.site.github import GitHub


class TestGithub(unittest.TestCase):
    def setUp(self):
        self.url = 'https://github.com/smp4903/FiveSecondRule'
        self.github = GitHub(self.url)

    def test_integration_github_find_zip_url(self):
        zip_url = self.github.find_zip_url()
        self.assertEqual(zip_url, f"https://github.com/smp4903/FiveSecondRule/archive/master.zip")

    def test_integration_github_get_addon_name(self):
        addon_name = self.github.get_addon_name()
        self.assertEqual(addon_name, 'FiveSecondRule')

    def test_integration_github_get_latest_version(self):
        latest_version = self.github.get_latest_version()
        self.assertRegex(latest_version, r"([a-f0-9]{7})")  # something like an abbreviated SHA-1 hash

    def test_github_get_supported_urls(self):
        supported_urls = self.github.get_supported_urls()
        self.assertIsNotNone(supported_urls)
        self.assertTrue(len(supported_urls) != 0)


if __name__ == '__main__':
    unittest.main()
