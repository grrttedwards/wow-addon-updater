import packages.requests as requests
from site.Site import Site


class WoWAce(Site):
    URL = 'https://www.wowace.com/projects/'

    def __init__(self, url: str):
        super().__init__(url)

    @classmethod
    def get_supported_urls(cls):
        return [cls.URL]

    def find_zip_url(self):
        return self.url + '/files/latest'

    def get_latest_version(self):
        try:
            page = requests.get(self.url + '/files')
            page.raise_for_status()  # Raise an exception for HTTP errors
            content_string = str(page.content)
            start_of_table = content_string.find('project-file-list-item')
            index_of_ver = content_string.find('data-name="', start_of_table) + 11  # first char of the version string
            end_tag = content_string.find('">', index_of_ver)  # ending tag after the version string
            return content_string[index_of_ver:end_tag].strip()
        except Exception:
            print(f"Failed to find version number for: {self.url}")
            raise
