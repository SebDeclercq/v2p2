from book_to_scrape.book_scraper import Book


def main() -> None:
    '''Main function'''
    book: Book = Book.fetch_and_create('a-light-in-the-attic_1000/')
    print(book)


if __name__ == '__main__':
    main()
