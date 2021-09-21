Title: Web Scraping Target Discovery: Search Bar
Date: 2021-09-19
Tags: discovery, python, scraping, reverse-engineering
Slug: web-scraping-discovery-search
Summary: Fundamental web-scraping reverse-engineering technique is figuring out how website's search works. Replicating web search in web scraping is a great target discovery technique. Why, when and how should it be used effectively?
toc: True
add_toc: True

Reverse engineering website's backend API is a common web-scraping technique - why scrape htmls when backend data can be scraped directly? In this article we'll briefly cover the most common web scraping reverse-engineering subject: the search bar.

## Using search API for web-scraping

One way to discovery targets in web scraping is to reverse-engineer the search bar for websites search API. It's often one of the best way to discover targets, let's overview common pros and cons of this approach.

Pros:

- __Fresh targets__: search API rarely yields links to outdated targets as it's exactly what website users see.  
- __Often good coverage__: search API can lead to all of the results site has to offer - if it's not searchable it's probably not there.
- __Often fast__: search API result pagination can yield 10-50 results per page and often can be scraped asynchronously. 

Cons:

- __Domain bound__: since every website has their own search structure the code can rarely be applied to many targets however.
- __Sometimes has page limits__: some search return limited amount of pages meaning the scraper has to figure out how to get around this limit which can be difficult to implement.
- __Sometimes slow__: some search result pagination cannot be iterated asynchronously. Pages need to be requested one after another which slows down scraping process.

As you can see pros and cons are very mixed and even contradicting - it really depends on websites search implementation. Lets cover few examples and see what search bar discovery is all about.

## Example: hm.com

For the first example lets see how a popular clothing website https://hm.com handles it's search. If you we go the website, open up our web inspector tools and search something we can see the search requests being made:

[% image src="hm.com-initial-req.png" %]

However this returns us filtered results when we want to discover all products on the website. For this we can trick the search API to search empty queries by either searching for empty string or a space. In this case no results are returned for an empty string `""` but we can force a space search by using url encoded character for space in the url bar: `%20`

[% image src="hm.com-space-search.png" %]

Success - we got 13780 product results! Now lets figure out how the search works. If you look at the inspector no data requests are made because first page data is embedded into HTML.

We could scrape HTMLs but we often we don't have to. Modern websites tend to communicate with backend API in JSON, so lets try to find that! If we scroll to the bottom of the page and click next page we can see actual JSON data request being made:

[% image src="hm.com-xhr-req.png" %]

Here we see the a request is being made to backend's search API and it returns us a json set of data with target urls as well as some metadata:

```json
```

Here we can see our search results and total results on the web-page. Having this information we can develop our scraping algorithm:

1. Get first page to get total result count.
2. Schedule request for all pages asynchronously.
3. Parse the pagination data asynchronously.

Here's quick implementation using Python with `httpx` request package:

```python
import httpx
import asyncio

async def scrape_page(limiter, query=" ",  offset=0, pagesize=40):
    url = f"https://www2.hm.com/en_us/search-results/_jcr_content/search.display.json?q=%20&department=1&sort=stock&image-size=small&image=stillLife&offset=40&page-size=40"
	return 
    ...
	 
async def main():
    url = """
    ...

if __name__ == "__main__":
    asyncio.run(main())
```

_Note: here using asyncio and httpx async session we can retrieve all data so quickly that we need to throttle ourselves with asyncio `Semaphore` - otherwise we're risking either getting our IP either throttled or suspend by the server._

If we run this simple scraping script we can see that our scanner will return TODONUMBER results. We can save these product urls into a queue, file or a database and later scrape product details!

## Summary and Further Reading

To summarize reverse engineering website's search API is a brilliant web target discovery technique however it's more difficult to develop as it requires reverse-engineer effort and all of the scrape code becomes very domain specific.   
From all discovery approaches covered in the ["Web Scraping Target Discovery"]() series this is probably the best one: it's efficient, has great coverage and with the right reverse-engineering skill set easy to develop.

-TODO-OUTRO-