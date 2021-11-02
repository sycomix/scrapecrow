Title: Web Scraping Target Discovery: Crawling
Date: 2021-09-28
Tags: discovery, crawling, intermediate, discovery-methods
Slug: web-scraping-discovery-crawling
Summary: The most common web scraping target discovery technique: recursive crawling. How does it work? What are the pros and cons and the most optimal execution patterns?
toc: True
add_toc: True

[% img-full src="banner-web.jpg" %]

{! content/partial/Web Scraping Target Discovery_intro.md !}

In this article we'll take a look at web crawling and how can we use it as a discovery strategy in web scraping.  

## What is recursive crawling and how is it used in web-scraping?

One of the most common ways to discover web scraping targets is to recursively crawl the website. This technique is usually used by broad scrapers (scrapers that scrape many different websites) and index crawlers such as Google and other search engine bots.  
In short crawling is recursive scraping technique where given a start url and some crawling rules the scraper continues exploring the website by visiting _all'ish_ of the links present on the website.  

To wrap our heads around crawling concept easier lets refer to this small flow chart:

[% img src="crawl-flow.png" %]

This flow chart illustrates the simplest domain-bound crawl spider flow: the crawler is given a starting point, it scrapes and parses it for urls present in the html body. Then applies matching rules to urls and determines whether to save to urls (for scraping later) or whether to follow them up to repeat the whole process.

Before using crawling as a web scraping discovery strategy it's a good practice to reflect on common pros and cons of this technique and see whether that would fit your web-scraping project:

Pros:  

- __Generic Algorithm__: can be applied to any website with few adjustments. In other words one web scraper can be adapted to any website quite easily.  
- __Good Coverage__: some websites (like e-commerce) are well interlinked thus crawling will have great discovery coverage.  
- __Easy to Develop__: no reverse-engineering skills are required since we're just falling natural website structure.  

Cons:  

- __Inefficient and Slow__: since crawling is a very generic solution it comes with a lot of inefficiencies. Often extracted links might not contain any product links so lots of crawl branches end up in dead ends.  
- __Insufficient Coverage__: some websites are not well interlinked (sometimes purposefully to prevent web scrapers). Crawlers can't discover items that are not referenced anywhere.  
- __Risk__: since scraped link bandwidth is much bigger than other discovery approaches the scrapers IPs are more likely to be throttled or blocked.  
- __Struggles With Javascript Heavy Websites__: since crawling is very generic and web scrapers don't execute javascript content (unless using browser emulation) some websites might be too complex for web scraper to follow.  

We can see that crawling is a smart generic way to discover scrape targets however it's not without it's faults: it's slower, less accurate and might be hard to accomplish with some javascript heavy websites.  
Lets take a look at example target discovery implementation that uses web crawling.

## Example Use Case: hm.com

Lets take a look at a popular clothing e-commerce website: <https://hm.com>. We'll be using crawling approach to find all clothing products on the website. 

First lets establish essential parts that make up a web crawler:

1. Link extractor - a function/object that can find urls in html body.
2. Defined link pattern rules to follow - a function/object that determines how to handle up extracted links.
3. Duplicate filter - object that keeps track of links scraper visited.
4. Limiter - since crawling visits many urls we need to limit connection rate to not overwhelm the website.  

These are 4 components that make up a basic web crawler. Lets see how we can implement them for hm.com.

### Crawling Rules

First lets establish our crawling rules. As per above flowchart our crawler needs to know which urls to follow up and which to save:

```
import re

class HMScraper:
    save_urls = re.compile("/productpage\.")  # e.g ...com/en_us/productpage.09008.html
    follow_urls = re.compile("\.html")
    follow_saved_urls = False
```

Here we defined our crawling rules:

- We want to save all urls that contain `/productpage.` in the url as all hm.com products follow this pattern  
- We want to follow up any url containing `.html`  
- Do not follow urls that are being saved.  

	Following saved urls can useful as product pages often contain "related products" urls which can help us increase discovery coverage. For hm.com domain this is unnecessary.  
	{:.info}

These are 3 rules that define our crawler's routine for domain `hm.com`. With that ready lets take a look how we can create a link extractor function that will use these rules to extract crawl targets.


### Crawl Loop

Having crawling rules defined we need to create a crawl loop that uses these rules to schedule a whole crawl process.   
In this example for our http processing we'll be using `httpx` and for html parsing `parsel` python packages. With these two tools we can define basic crawler skeleton:


```python
import logging
import asyncio
import re
from urllib.parse import urlparse
from typing import List
from parsel import Selector
from httpx import AsyncClient


class HMScraper:
    save_urls = re.compile("/productpage\.")  # e.g ...com/en_us/productpage.09008.html
    follow_urls = re.compile("\.html")
    follow_saved_urls = False

    def __init__(self, limit=5):
		# asyncio.Semaphore object allows us to limit coroutine concurrency 
		# in our case we can limit how many concurrent requests are being made
        self.limiter = asyncio.Semaphore(limit)
        self.seen_urls = set()

    async def __aenter__(self):
        """on scraper creation open http session"""
        self.session = AsyncClient(
            # we should use a browser-like user agent header to avoid being blocked
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
            }
        )
        return self

    async def __aexit__(self, *args):
        """on scraper destruction close http session"""
        await self.session.aclose()

    async def _request(self, url: str):
	    """our http request wrapper function that implements rate limiting"""
        async with self.limiter:
            try:
                resp = await self.session.get(url)
            except Exception as e:
                return e
            return resp
	
	async def save(self, url):
		# for display purposes lets just print the url
		print(url)
	
	async def scrape(self):
		...

	async def find_links(self, response):
	    ...
```

With this skeleton, we have basic usage API for our scraper. We can define our run function:

```python
async def run():
    async with HMScraper() as scraper:
        start_urls = [
            # homepage for US website
            "https://www2.hm.com/en_us/index.html"
        ]


if __name__ == "__main__":
    asyncio.run(run())
```

Great! Now all we have to do is fill in the interesting bits: link extraction and scrape loop.  
For scrape loop all we need to do is request urls, find links in them, follow or save ones that match our rules:

```python
    async def scrape(self, urls: List[str]):
        """Breadth first"""
        while True:
            to_follow = set()
            for resp in asyncio.as_completed([self._request(url) for url in urls]):
				try:
					resp = await resp
				# skip failed requests; ideally this should be retried or logged
				except Exception:
					continue
                if resp.status_code != 200:
                    continue

                for url in self.find_links(resp.text):
                    if self.save_urls.search(url):
                        await self.save(url)
                        if not self.follow_saved_urls:
                            continue
                    if self.follow_urls.search(url):
                        print(f"  following {url}")
                        to_follow.add(url)
            if to_follow:
                urls = to_follow
            else:
                return  # end of the crawl
```

Here we've defined an "endless" while loop that does exactly that: get htmls, parse them for urls where we store some of them and follow up the others. The last remaining piece is our link extraction logic.   

### Link Extracting

Link extraction process is the core part that makes the crawler and can get quite complex in logic. For our example domain `hm.com` it's relatively simple. We'll find all urls in the page by following `<a>` nodes:

```python
    def find_links(self, resp, only_unique=True):
        # build a parsable tree from html body
        sel = Selector(resp.text)
        current_url_parts = urlparse(resp.url)
        # find all <a> nodes and select their href attribute
        urls = sel.xpath("//a/@href").extract()
        for url in urls:
            # convert relative url to absolute
            if url.startswith("/"):
                url = current_url_parts._replace(path=url).geturl()
            # skip absolute urls that do not match current domain
            if urlparse(url).netloc != current_url_parts.netloc:
                continue
            # skip visited urls
            if only_unique and url in self.seen_urls:
                continue
            self.seen_urls.add(url)
            yield url
```

Here we first build a tree parser object to get all those `<a>` node links. Then we iterate through them and filter out anything that is not an url of this website or has been visited already.

Link Extraction can get complicated very quickly as some website can contain non-html files (e.g. `/document.pdf`) that need to be filtered out and many other niche scenarios. 
{:.info}

With link extraction complete, we can put together our whole crawler into once piece and see how it performs!

### Putting It All Together

Now that we have all parts complete: crawl loop, link extraction, link matching and request limiting. Let's put it all together and run it:

```python
{! content/examples/discovery-crawl.py !}
```

If we run our crawler we'll notice few things:
- At time of writing 13800~ results are being found which matches well with our other [#discovery-methods] used in this blog series.
- It took a while to complete this crawl: TODO second. Since we are crawling so many pages compared to other discovery methods we crawl 

Finally, we can see that we can easily reuse most of this scraper for other websites, all we need to do is change our rules! That's the big selling point of crawlers, is that they're less domain specific than individual web scrapers.

## Summary and Further Reading

To summarize, web crawling is a great discovery technique that lends easily to generic/broad scraper development because the same scrape loop can be applied to many targets just with some rule adjustments. However it's less efficient - slower and riskier when it comes to blocks - than other discovery techniques like [Search Bar] or [Sitemaps]. 

{! content/partial/Web Scraping Target Discovery_outro.md !}

The code used in this article can be found on [github][code-github].  
{:.info}

[scraper-source]: http://github.com
[Sitemaps]: /web-scraping-discover-sitemaps.html
[Search Bar]: /web-scraping-discover-search.html
[code-github]: https://github.com/Granitosaurus/scrapecrow/tree/main/examples