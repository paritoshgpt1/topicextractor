import sys

from WebScraper import WebScraper

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Invalid Number of Arguments. Please refer to the README for usage instructions.")
    else:
        url = sys.argv[1]
        scraper = WebScraper(url)
        response = scraper.extract()
        if response is None:
            print("Error fetching the data from the URL provided")
        else:
            print(response)
