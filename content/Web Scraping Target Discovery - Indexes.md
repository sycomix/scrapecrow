Title: Web Scraping Target Discovery: Indexes
Date: 2021-09-19
Tags: discovery, python, scraping
Slug: web-scraping-discovery-indexes
Summary: The most common web scraping target discovery technique: recursive crawling. How does it work? What are the pros and cons and the most optimal execution paterns?
toc: True
add_toc: True

Using various public indexers is a often viable target discovery strategy. It is mostly used as a last resort or as a supplementary technique for difficult discovery-difficult targets.  
Public indexers that crawl the web through more complex scraping rules might pickup hard to find targets and we can take advantage of that in our little web scraper. In other words as the spirit of web-scraping goes: it's smart to take advantage of existing work! In this article we'll take a look at few common public indexers and how can we use them to discover targets.

Pros:

- __Easy__: once understood taking advantage of public indexers is surprisingly easy.
- __Efficient__: public indexes function similar to in-website search bars or often come in easy to parse data dumps that we don't even need connection to discover targets.

Cons:

- __Insufficient coverage and stale data__: because these are indexes gathered whenever and by whatever there's very little coverage and link quality. For this reason it is best to combine index based discovery with some other discovery techniques.

## Search Engines 

Most common and rich public indexes are search engines like google, bing or duckduckgo anything that lets humans search the web can be a useful tool for web scraping robots as well.  

To see how we would use search engine in web-scraping discover lets take example of https://crunchbase.com. We want to scrape their company data and to discover companies we can use a public search engine. In this example we'll use bing.com because it's easy to web-scrape (unlike google which employs various anti-scraping strategies).  

If we take a look at an average crunchbase company page like https://www.crunchbase.com/organization/linkedin we can determine an url pattern that all company pages follow: `/organization/<name>`  
Knowing this we can write domain specific queries in bing.com search box:

[% image src=bing.com-crunchbase-search.png %]

Here we used query `/organization/ site:crunchbase.com` and bing.com is giving us over a million of results which is pretty close to what the crunchbase is saying they have!   

Other search engines like google, duckduckgo and such also support similar search syntax. Search can be refined even further with more advanced search rules, e.g. [bing's advanced search options](https://help.bing.microsoft.com/#apex/bing/en-US/10001/-1) and [bing's advanced search keywords](https://help.bing.microsoft.com/#apex/bing/en-US/10001/-1) can be combined to create some useful discovery queries.

Using search engines to query is not without it's faults. They are often built for humans rather than robots and have limited pagination (i.e. query will only have 10 pages of results even though it says millions are found) which requires splitting single query into many smaller ones, e.g. searching every letter of the alphabet or particular names. That being said this discovery approach is surprisingly easy and can often work beautifully!

## Public Index Dumps

There are several public web indexes but probably the biggest and most well known one is https://commoncrawl.org/ which crawls the web and provides data dumps for free. Unfortunately this being an open and free project the crawled htmls are somewhat stale, though as web scraper engineers we can instead use it as an index feed for our web scrapers.

You can access common crawl's web index here: http://urlsearch.commoncrawl.org/. The data is grouped by months and can be experimented in individual month search playground they have:

[% image src=commoncrawl-crunchbase-search.png %]

However this data often comes in handy and it's useful just to have it around on your hard-drive or local database - so downloading all indexes is highly recommended! 

# Summary and Further Reading

To summarize using public indexes can be a valid scrape target discovery technique however it's best used to supplement other discovery techniques because of inferior coverage and data quality.  

--TODO-OUTRO--