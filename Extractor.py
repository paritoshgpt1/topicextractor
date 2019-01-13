import sys

from WebScraper import WebScraper

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Invalid Number of Arguments. Please enter a URL")
    else:
        url = sys.argv[1]
        scraper = WebScraper(url)
        response = scraper.extract()
        if response is None:
            print("Error fetching the data from the URL provided")
        else:
            print(response)
