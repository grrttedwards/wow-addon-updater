import re

import packages.requests as requests
from site.AbstractSite import Site


class Tukui(Site):
    URL = 'https://git.tukui.org'

    def __init__(self, url: str):
        super().__init__(url)

    @classmethod
    def get_supported_urls(cls) -> [str]:
        return [cls.URL]

    def find_zip_url(self):
        return self.url + '/-/archive/master/elvui-master.zip'

    def get_latest_version(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            content = str(response.content)
            match = re.search(
                r'<div class="commit-sha-group">\\n<div class="label label-monospace">\\n(?P<hash>[^<]+?)\\n</div>',
                content)
            result = ''
            if match:
                result = match.group('hash')
            return result.strip()
        except Exception:
            print(f"Failed to find version number for: {self.url}")
            raise
