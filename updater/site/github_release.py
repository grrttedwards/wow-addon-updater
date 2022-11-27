import requests
import re
from bs4 import BeautifulSoup

from typing import Dict, Optional
from updater.site.abstract_site import AbstractSite
from updater.site.github import GitHub
from updater.site.enum import GameVersion


class GitHubRelease(AbstractSite):
    _URLS = ['https://www.github.com/', 'https://github.com/']

    session = requests.session()

    def __init__(self, url: str, credentials: Optional[Dict[str, str]]):
        self.headers = {}
        if credentials and (token := credentials.get("token")):
            self.headers["authorization"] = f"token {token}"
        super().__init__(url, GameVersion.agnostic)

    @classmethod
    def handles(cls, url: str) -> bool:
        return bool(re.match('^https://(www\.)?github\.com/[^/]+/[^/]+/releases/?$', url))

    def find_zip_url(self):
        try:
            repo = self._get_repo_name()
            response = GitHubRelease.session.get(
                f'https://api.github.com/repos/{repo}/releases',
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            # First zip file asset in a non-prerelease
            for entry in data:
                if not entry['draft'] and not entry['prerelease']:
                    for asset in entry['assets']:
                        if asset['content_type'] in {'application/zip', 'application/x-zip-compressed'}:
                            return asset['browser_download_url']
        except Exception as e:
            raise self.download_error() from e
        raise self.download_error()

    def _get_repo_name(self):
        _, owner, repo, _ = self.url.replace('https://', "", 1).split('/', 4)
        return f'{owner}/{repo}'

    def get_latest_version(self):
        try:
            repo = self._get_repo_name()
            response = GitHubRelease.session.get(
                f'https://api.github.com/repos/{repo}/releases',
                headers=self.headers,
            )
            response.raise_for_status()
            data = response.json()
            for entry in data:
                if not entry['draft'] and not entry['prerelease']:
                    return entry['tag_name']
        except Exception as e:
            raise self.version_error() from e
        raise self.version_error()

    def get_addon_name(self):
        return self._get_repo_name().split('/')[-1]
