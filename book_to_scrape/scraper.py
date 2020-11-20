from typing import ClassVar, Iterator, Union
import re
from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import Response
import requests
from requests.api import request


class Scraper:
    BASE_URL: ClassVar[str] = 'http://books.toscrape.com/'
    CATALOGUE_URL: ClassVar[str] = BASE_URL + 'catalogue/'

    @classmethod
    def fetch(cls, url: str) -> Response:
        return requests.get(cls.CATALOGUE_URL + url)

    @classmethod
    def fetch_category_list(cls) -> Iterator[str]:
        with requests.get(cls.BASE_URL) as resp:
            soup: BeautifulSoup = BeautifulSoup(resp.content, 'html.parser')
            categories: Tag = soup.find('div', class_='side_categories').find(
                'ul'
            )
            for category in re.split(r'\n+', categories.text):
                if category := category.strip():
                    yield category
