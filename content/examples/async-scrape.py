import asyncio
from time import time
from httpx import AsyncClient


async def scrape(url, session):
    return await session.get(url)


async def run():
    _start = time()
    async with AsyncClient() as session:
        # this url will always take 1 second
        url = "http://httpbin.org/delay/1"
        tasks = [scrape(url, session=session) for _ in range(100)]
        results = await asyncio.gather(*tasks)
    print(f"finished scraping in: {time() - _start:.1f} seconds")


if __name__ == "__main__":
    asyncio.run(run())
