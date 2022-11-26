import unittest
import os

from updater.site.github_release import GitHubRelease


class TestGithubRelease(unittest.TestCase):
    def setUp(self):
        self.url = "https://github.com/smp4903/FiveSecondRule/releases"
        credentials = None
        if token := os.environ.get("GITHUB_TOKEN"):
            credentials = {"token": token}
        self.github = GitHubRelease(self.url, credentials)

    def test_integration_github_find_zip_url(self):
        zip_url = self.github.find_zip_url()
        self.assertRegex(
            zip_url,
            r"^https://github\.com/smp4903/FiveSecondRule/releases/download/.+\.zip$",
        )

    def test_integration_github_get_addon_name(self):
        addon_name = self.github.get_addon_name()
        self.assertEqual(addon_name, "FiveSecondRule")

    def test_integration_github_get_latest_version(self):
        latest_version = self.github.get_latest_version()
        self.assertIsInstance(latest_version, str)
        self.assertNotEqual(latest_version, "")

    def test_github_get_supported_urls(self):
        supported_urls = self.github.get_supported_urls()
        self.assertIsNotNone(supported_urls)
        self.assertTrue(len(supported_urls) != 0)


if __name__ == "__main__":
    unittest.main()
