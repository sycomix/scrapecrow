from httpx import Client
from time import time


def scrape(url, session):
    return session.get(url)


def run():
    _start = time()
    results = []
    with Client() as session:
        # this url will always take 1 second
        url = "http://httpbin.org/delay/1"
        results.extend(scrape(url, session=session) for _ in range(100))
    print(f"finished scraping in: {time() - _start:.1f} seconds")


if __name__ == "__main__":
    run()
