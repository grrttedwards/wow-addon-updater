import requests

from updater.site.AbstractSite import AbstractSite


class Curse(AbstractSite):
    OLD_CURSE_URL = 'https://mods.curse.com/addons/wow/'
    OLD_PROJECT_URL = 'https://wow.curseforge.com/projects/'
    MAIN_URL = 'https://www.curseforge.com/wow/addons/'

    def __init__(self, url: str):
        url = convert_old_curse_urls(url)
        super().__init__(url)

    @classmethod
    def get_supported_urls(cls):
        return [cls.OLD_CURSE_URL, cls.OLD_PROJECT_URL, cls.MAIN_URL]

    def find_zip_url(self):
        try:
            page = requests.get(self.url + '/download')
            page.raise_for_status()  # Raise an exception for HTTP errors
            content_string = str(page.content)
            # Will be the index of the first char of the url
            index_of_ziploc = content_string.find('PublicProjectDownload.countdown') + 33
            end_quote = content_string.find('"', index_of_ziploc)  # Will be the index of the ending quote after the url
            return 'https://www.curseforge.com' + content_string[index_of_ziploc:end_quote]
        except Exception:
            print('Failed to find downloadable zip file for addon. Skipping...\n')
            raise

    def get_latest_version(self):
        try:
            page = requests.get(self.url + '/files')
            page.raise_for_status()  # Raise an exception for HTTP errors
            content_string = str(page.content)
            index_of_ver = content_string.find(
                '<h3 class="text-primary-500 text-lg">') + 37  # first char of the version string
            end_tag = content_string.find('</h3>', index_of_ver)  # ending tag after the version string
            return content_string[index_of_ver:end_tag].strip()
        except Exception:
            # print('Failed to find version number for: ' + self.url)
            raise Exception('Failed to find version number for: ' + self.url)


def convert_old_curse_urls(url: str):
    if any(old_url in url for old_url in [Curse.OLD_CURSE_URL, Curse.OLD_PROJECT_URL]):
        try:
            # Some old URL's may point to nonexistent pages. Rather than guess at what the new
            # name and URL is, just try to load the old URL and see where Curse redirects us to.
            page = requests.get(url)
            page.raise_for_status()
            return page.url
        except Exception:
            print(f"Failed to find the current page for old URL [{url}]. Skipping...\n")
            raise
    else:
        return url
