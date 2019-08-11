import packages.requests as requests
from updater.site.AbstractSite import AbstractSite


class WoWInterface(AbstractSite):
    URL = 'https://www.wowinterface.com/downloads/'

    def __init__(self, url: str):
        super().__init__(url)

    @classmethod
    def get_supported_urls(cls) -> [str]:
        return [cls.URL]

    def find_zip_url(self):
        downloadpage = self.url.replace('info', 'download')
        try:
            page = requests.get(downloadpage + '/download')
            page.raise_for_status()  # Raise an exception for HTTP errors
            content_string = str(page.content)
            index_of_ziploc = content_string.find('Problems with the download? <a href="') + 37  # first char of the url
            end_quote = content_string.find('"', index_of_ziploc)  # ending quote after the url
            return content_string[index_of_ziploc:end_quote]
        except Exception:
            print('Failed to find downloadable zip file for addon. Skipping...\n')
            raise

    def get_latest_version(self):
        try:
            page = requests.get(self.url)
            page.raise_for_status()  # Raise an exception for HTTP errors
            content_string = str(page.content)
            index_of_ver = content_string.find('id="version"') + 22  # first char of the version string
            end_tag = content_string.find('</div>', index_of_ver)  # ending tag after the version string
            return content_string[index_of_ver:end_tag].strip()
        except Exception:
            print('Failed to find version number for: ' + self.url)
            raise
