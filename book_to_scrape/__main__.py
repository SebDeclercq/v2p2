from book_to_scrape.book_scraper import Book
from book_to_scrape.category_scraper import Category
from book_to_scrape.scraper import Scraper


def main() -> None:
    '''Main function'''
    book: Book = Book.fetch_and_create('a-light-in-the-attic_1000/')
    print(book)
    for category in Scraper.fetch_category_list():
        print(category)


if __name__ == '__main__':
    main()
