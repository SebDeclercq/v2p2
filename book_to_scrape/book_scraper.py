from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Union
import re
from bs4 import BeautifulSoup
from bs4.element import Tag
from requests import Response
from book_to_scrape.scraper import Scraper


BookMetadata = Dict[str, Union[float, int, str]]


@dataclass
class Book(Scraper):
    product_page_url: str
    universal_product_code: str
    title: str
    price_including_tax: float
    price_excluding_tax: float
    number_available: int
    product_description: str
    category: str
    review_rating: int
    image_url: str

    RATING_MAPPING: ClassVar[Dict[str, int]] = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
    }

    @property
    def as_dict(self) -> BookMetadata:
        return asdict(self)

    @classmethod
    def fetch_and_create(cls, url: str) -> Book:
        metadata: BookMetadata = {'product_page_url': cls.CATALOGUE_URL + url}
        metadata.update(cls.parse_response(cls.fetch(url)))
        return cls(**metadata)  # type: ignore

    @classmethod
    def parse_response(cls, resp: Response) -> BookMetadata:
        soup: BeautifulSoup = BeautifulSoup(resp.content, 'html.parser')
        metadata_table: Tag = soup.find('table', class_='table table-striped')
        return dict(
            title=cls.get_title(soup),
            universal_product_code=cls.get_upc(metadata_table),
            price_including_tax=cls.get_price_incl_tax(metadata_table),
            price_excluding_tax=cls.get_price_excl_tax(metadata_table),
            number_available=cls.get_number_available(soup),
            product_description=cls.get_description(soup),
            category=cls.get_category(soup),
            review_rating=cls.get_review_rating(soup),
            image_url=cls.get_image_url(soup),
        )

    @staticmethod
    def get_title(soup: BeautifulSoup) -> str:
        return soup.find('div', class_='product_main').h1.text

    @classmethod
    def get_upc(cls, metadata_table: Tag) -> str:
        return cls.get_metadata_by_text('UPC', metadata_table)

    @classmethod
    def get_price_incl_tax(cls, metadata_table: Tag) -> float:
        return float(
            cls.get_metadata_by_text('Price (incl. tax)', metadata_table)[1:]
        )

    @classmethod
    def get_price_excl_tax(cls, metadata_table: Tag) -> float:
        return float(
            cls.get_metadata_by_text('Price (excl. tax)', metadata_table)[1:]
        )

    @staticmethod
    def get_metadata_by_text(text: str, metadata_table: Tag) -> str:
        return metadata_table.find('th', text=text).find_next('td').text

    @staticmethod
    def get_number_available(soup: BeautifulSoup) -> int:
        return int(
            re.search(
                r'\d+', soup.find('p', class_='instock availability').text
            ).group(0)
        )

    @staticmethod
    def get_description(soup: BeautifulSoup) -> str:
        return soup.find('div', id='product_description').find_next('p').text

    @staticmethod
    def get_category(soup: BeautifulSoup) -> str:
        return (
            soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
        )

    @classmethod
    def get_review_rating(cls, soup: BeautifulSoup) -> int:
        return cls.RATING_MAPPING[
            soup.find('p', class_='star-rating')['class'][1].lower()
        ]

    @classmethod
    def get_image_url(cls, soup: BeautifulSoup) -> str:
        url: str = (
            soup.find('div', class_='thumbnail')
            .find('img')['src']
            .replace('../', '')
        )
        return cls.BASE_URL + url
