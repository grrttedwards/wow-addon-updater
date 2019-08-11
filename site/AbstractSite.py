from abc import ABC, abstractmethod


class Site(ABC):
    def __init__(self, url: str):
        self.url = url

    @classmethod
    def handles(cls, url: str) -> bool:
        return any(supported_url in url for supported_url in cls.get_supported_urls())

    @classmethod
    @abstractmethod
    def get_supported_urls(cls) -> [str]:
        # ABC for some reason won't enforce implementing this, perhaps
        # because it only checks when the class is instantiated?
        raise TypeError(f"Can't instantiate abstract class {cls.__name__}"
                        " with abstract methods get_supported_urls")

    @abstractmethod
    def find_zip_url(self) -> str:
        pass

    @abstractmethod
    def get_latest_version(self) -> str:
        pass

    def get_addon_name(self) -> str:
        name = self.url
        for url in self.get_supported_urls():
            name = name.replace(url, '')
        return name
