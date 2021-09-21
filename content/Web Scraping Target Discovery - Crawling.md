Title: Web Scraping Target Discovery: Crawling
Date: 2021-09-19
Tags: discovery, python, scraping
Slug: web-scraping-discovery-crawling
Summary: The most common web scraping target discovery technique: recursive crawling. How does it work? What are the pros and cons and the most optimal execution paterns?
toc: True
add_toc: True

## What is recursive crawling and how is it used in web-scraping?

One of the most common ways to discover web scraping targets is to recursively crawl the website. This technique is usually used by broad crawlers and indexers such as Google and other search engine bots.   
In short crawling is recursive scraping technique where given a start url the scraper continues exploring the whole website by continuing to following found links until every link is visited.

```
                             ┌─────────────────┐
                             │ Start URL Pool  │
                             └────────┬────────┘
                                      │
                             ┌────────▼────────┐
         ┌───────────────────►    GET urls     ◄────────────────┐
         │                   └────────┬────────┘                │
         │                            │                         │
         │                            │                         │
         │                            │                         │
┌────────┴───────────┐      ┌─────────▼──────────┐              │
│ Parse Product Data │      │ Parse for relative │              │
└────────▲───────────┘      │       links        │              │
         │                  └─────────┬──────────┘              │
         │                            │                         │
         │                            │                         │
         │                  ┌─────────▼──────────┐              │
         └──────────────────┤  Duplicate Filter  ├──────────────┘
       URL is a product url └────────────────────┘ URL is a non-product like
```

This flow chart illustrates the simplest domain-bound crawl spider flow. Where scrape program is designed in a way to explore the whole website.  

Before using sitemaps a web scraping discovery strategy it's a good practice to reflect on common pros and cons of this technique and see whether that would fit a web-scraping project:

<u>Pros</u>:  

- __Generic Algorithm__: can be applied to any website with few adjustments. In other words one web scraper can be adapted to any website just   
- __Potentially Good Coverage__: some websites (like e-commerce) are well interlinked thus crawling will have great coverage.  
- __Easy to develop__: no reverse-engineering skills are required since we're just falling natural website structure.  

<u>Cons</u>:  

- __Inefficient and Slow__: since crawling is a very generic solution it comes with a lot of inefficiencies. Often extracted links might not contain any product links so lots of crawl branches end up in dead ends.  
- __Insufficient Coverage__: some websites are not well interlinked and sometimes purposefully to prevent web scrapers. Discovery via crawling might yield insufficient coverage.    
- __IP ban/block possibilities__: since scraped link bandwidth is much bigger than other discovery approaches the scrapers IPs are more likely to be throttled or blocked.  
- __Struggles with javascript heavy websites__: since crawling is very generic and web scrapers often don't execute javascript content might be too complex for web scraper to follow.  

We can see that crawling is a smart generic way to discover scrape targets however it's not without it's faults: it's slower, less accurate and might be hard to accomplish with some javascript heavy websites.  
Lets take a look at example target discovery implementation that uses web crawling.

## Example Use Case: hm.com

Lets take a look at a popular clothing e-commerce website: <https://hm.com>. We'll be using crawling approach to find all men clothing products on the website. For this we'll need 3 key pieces in our web scraper:

1. Link extractor - a function/object that can find urls in html body.
2. Defined link pattern rules to follow - a function/object that determines how to follow up extracted links.
3. Duplicate filter - object that keeps track of links scraper visited.

These are 3 core principles of a basic crawler. Lets see them in action!  

### Extracting Links

First lets start with link extractor. We'll make a class for linkextractor object that takes html text and finds all relative links in it. For this we'll use `parsel` html tree parsing package and some simple [xpath selectors]():

```python
from parsel import Selector

class HMScraper:
    """Product scraper of hm.com"""
    domain = "hm.com"
	
    def __init__(self):
		self.log = logging.getLogger(type(self).__name__)
		
    def find_links(self, html):
	    """
        find all relative page links in html link nodes
        """
		# build a parsable tree from html body
	    sel = Selector(html)
		# find all <a> nodes and select their href attribute
		urls = sel.xpath("//a/@href").extract()
		for url in urls:
		    # urls that start with / are relative urls
		    if url.startswith("/"):
			    yield url
			elif self.domain in url:
			    yield url
            else:
			    self.log.debug(f"skipping {url}")
			    
```

This simplified link extractor will parse html `<a>` nodes and find all relative links that either start with `/` or contain current domain.   

### Avoiding Duplicates

Now we can take advantage of this link extractor and implement de-duplication function to our scraper class. Deduplication is vital for preventing redundant crawling and potentially endless loops. The most basic deduplication method is just to keep track visited urls in memory:

```python
    def __init__(self):
	    self.log = logging.getLogger(type(self).__name__)
        # keep memory of all seen urls
		self.seen_urls = set()
		
    def find_unique_links(self, html):
        """
		find only unique relative links
        """
	    for url in self.find_links(html):
            # skip seen urls
		    if url in self.seen:
			    continue
            # otherwise show unseen urls and mark them as seen
			self.seen_urls.add(url)
			yield url
```

Here we can take advantage of python sets to keep track of links we've seen and only extract unseen ones from html body. 

### Scrape Loop

With link extraction configured we can write our main scraping loop. In short we want to scrape initial urls, parse their data and find follow links in which we'll repeat the whole process. The loop should end once no new links to follow can be found:

```python
    async def scrape(urls: List[str]):
	    responses = await asyncio.gather([
		    self.session.get(url)
			for url in urls
		])
        
		more_urls = set()
		for resp in responses:
		    more_urls.union(set(self.find_unique_links(resp.text)))
```

Full scraping loop...

<info>full code with additional comments for this scraper can be found [here][scraper-source]</info>

## Summary and Further Reading

To summarize web crawling is a great discovery technique that lends easily to generic/broad scraper development. However it's less efficient than other discovery techniques like [Search Bar]() or [Sitemaps]() and might not yield as great of a coverage.   
It often works the best with e-commerce websites or targets that are heavily interlinked and referenced through out the website. 

-TODO-OUTRO-

[scraper-source]: http://github.com