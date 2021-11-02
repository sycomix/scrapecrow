Title: Web Scraping Target Discovery
Date: 2021-09-29
Tags: discovery, python, crawling
Slug: web-scraping-discovery
Summary: Target discovery in web-scraping is how the scraper explores target website to find scraping targets. For example to scrape product data of an e-commerce website we would need to find urls to each individual product. This step is called "discovery". What types of discovery methods are there?

[% img-full src="banner-telescopes.png" %]

{! content/partial/Web Scraping Target Discovery_intro.md !}

In this blog series tagged [#discovery-methods] we'll take a look at common discovery methods used in web-scraping where each is different enough to have it's own risks, negatives and benefits. We'll target an example clothing store website <https://hm.com> for all of these discovery approaches:

- [Sitemaps] - using website sitemap indexes.
- [Search API] - reverse engineering websites search api.
- [Indexes] - taking advantage of existing indexes and search engines.
- [Crawling] - recursively scrape whole website to find what we're looking for.

These are 4 main discovery approaches that can be used in web scraping target discovery and knowing them is a great tool in web scraper developers utility belt.  
To quickly summarize our 4 main articles the discovery strategies vary quite a bit:

- __Sitemaps__ is probably the best approach as it's fast, safe and easy to implement; however unfortunately sitemaps of many websites are often neglected or contain dated links.  
- Reverse engineering websites __search api__ on the other hand is both efficient and has great results; however it requires reverse-engineering knowledge and can be difficult/time consuming to implement.   
- __Crawling__ is a great general approach but it's risky, slow and resource intensive.  
- Finally taking advantage of __existing indexes__ is a great last resort for web-sites that don't like to be scraped as they still want to be indexed by search engines or other indexers.

So which one to use? It really depends on your target and resources.   
Hopefully this extensive blog series can help you determine the right way to find your data targets!

{! content/partial/Web Scraping Target Discovery_outro.md !}

---
<figcaption>image credits: "Telescopes, Mauna Kea, Hawaii" by Gregory Williams is licensed under CC BY-NC-ND 2.0</figcaption>

[Sitemaps]: /web-scraping-discovery-sitemaps.html
[Search API]: /web-scraping-discovery-search.html
[Indexes]: /web-scraping-discovery-indexes.html
[Crawling]: /web-scraping-discovery-crawling.html