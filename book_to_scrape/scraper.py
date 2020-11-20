from typing import ClassVar
from requests import Response
import requests


class Scraper:
    BASE_URL: ClassVar[str] = 'http://books.toscrape.com/'
    CATALOGUE_URL: ClassVar[str] = BASE_URL + 'catalogue/'

    @classmethod
    def fetch(cls, url: str) -> Response:
        return requests.get(cls.CATALOGUE_URL + url)
