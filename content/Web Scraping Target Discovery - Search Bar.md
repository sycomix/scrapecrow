Title: Web Scraping Target Discovery: Search API
Date: 2021-09-28
Tags: discovery, discovery-methods, python, reverse-engineering
Slug: web-scraping-discovery-search
Summary: Fundamental web-scraping reverse-engineering technique is figuring out how website's search works. Replicating web search in web scraping is a great target discovery technique. Why, when and how should it be used effectively?
toc: True
add_toc: True

{! content/partial/Web Scraping Target Discovery_intro.md !}

Reverse engineering website's backend API is a common web-scraping technique - why scrape htmls when backend data can be scraped directly? In this article we'll briefly cover the most common web scraping reverse-engineering subject: the search API.


## Using search API for web-scraping

One way to discovery targets in web scraping is to reverse-engineer the search bar for websites search API. It's often one of the best ways to discover targets - let's overview common pros and cons of this approach:

Pros:

- __Fresh Targets__: search API rarely yields links to outdated targets as it's exactly what website users see.  
- __Good Coverage__: search API can lead to all of the results site has to offer - if it's not searchable it's probably not there.
- __Efficient__: search API result pagination can yield 10-50 results per page and often can be scraped asynchronously. 

Cons:

- __Domain bound__: since every website has their own search structure the code can rarely be applied to many targets however.
- __Limited Coverage__: some search return limited amount of pages (e.g. there are 900 results but after 10 pages the API does not provide any results) meaning the scraper has to figure out how to get around this limit which can be difficult to implement.
- __Slow__: Rarely but some search result pagination cannot be iterated asynchronously. Pages need to be requested one after another which slows down scraping process.

As you can see pros and cons are very mixed and even contradicting - it really depends on websites search implementation. Lets cover few examples and see what search API discovery is all about.

## Example: hm.com

To understand basic search bar reverse-engineering lets see how a popular clothing website <https://hm.com> handles it's search. 

### Reversing Search Bar

If we go the website, open up our web inspector tools and search something we can see the search requests being made by the browser:

[% img-big src="hm.com-initial-req.png" %]

However this returns us filtered results when we want to discover _all_ products on the website.   
For this we can trick the search API to search empty queries by either searching for empty string or a space character. In this case no results are returned for an empty string `""` but we can force this search by using url encoded (also called "percent encoded") character for space in the url bar: `%20`

For more on percent encoding see [MDN's documentation](https://developer.mozilla.org/en-US/docs/Glossary/percent-encoding).
{:.info}

[% img-big src="hm.com-space-search.png" %]

Success! We got 13780 product results!   
Now lets figure out how the search works. If you look at the inspector no data requests are made, because first page data is embedded into HTML as a javascript variable - this is a common website optimization that we can ignore.

We could scrape HTMLs but we often we don't have to. Modern websites tend to communicate with backend API in JSON, so lets try to find that.   
If we scroll to the bottom of the page and click next page we can see actual JSON data request being made for the second page:

[% img-big src="hm.com-xhr-req.png" %]

We see a request is being made to backend's search API and it returns us a json set of data with product metadata and location. Let's take a look at the request url so we can replicate it in our scrapper:

```
https://www2.hm.com/en_us/search-results/_jcr_content/search.display.json?
q=%20&   # search term
offset=0&  # pagination offset
page-size=40&   # pagination limit
sort=ascPrice  # sort type
```

Many modern web APIs are very flexible with parameters - we don't have to use all of the junk we see in our web inspector. You can always experiment and see which are necessary and how the content changes when parameters do.  
In this example we stripped off a lot of uninteresting parameters and just kept query,offset/limit and sort
{:.info}

This seems like a common offset/limit pagination technique. Which is great for web-scrapers as we can get multiple pages asynchronously - in other words we can requests slices 0:100, 100:200, ... concurrently.

### Confirming Pagination

Before we can commit to using this API endpoint we should test it for common coverage pitfalls, for example for page limits. Often search APIs limit amount of rows/pages query can request. If we just click the link in the browser:

<https://www2.hm.com/en_us/search-results/_jcr_content/search.display.json?q=%20&offset=0&page-size=40&sort=ascPrice>

We can see json response and total of results count of `13_730`.  
Let's see if we can get last page which at the time of this article would be: `offset=13690&page-size=40`:

<https://www2.hm.com/en_us/search-results/_jcr_content/search.display.json?q=%20&offset=13690&page-size=40&sort=ascPrice>

Unfortunately while requests is successful it contains no product data, indicated as empty array: `"products": []`   

It's what we feared and this pagination has a page limit. By messing around with the parameter we can find where the pagination ends exactly and thats at `10_000` results, which is not an uncommon round number.    

Lets see of few common ways we could get around this pagination limit:

1. Use multiple search queries - common brute force technique is searching many different queries like: `a`, `b`, `c`... and hope all of the products are found.
2. Apply more filters - this query allows optional filter such as categories. We can collect all categories, e.g. `shoes`, `dresses` etc. and have query for every one of them.  
3. We can reverse sorting - if one query can give us 10_000 results, by reversing sorting we can have 2 queries with 10_000 results each! That's an easy way to double our reach.  

For this specific case seems like approach #3 Reversing Sorting is the best approach! As the website only has a bit over 13_000 results and our reach would be 20_000 - this would be a perfect solution.   
We can sort our query by price and reach for results from both ends of the query:

[% img-big src="hm.com-double-end-query.png" %]

So our first query would get us first 10_000 cheapest items and second query would pick up first 3_700 most expensive items. With these two queries we can fully discover all available products.

### Implementation

Having reverse engineering how search API of hm.com works we can develop our scraping algorithm:

1. Get first page to get total result count.
2. Schedule request for first `10_000` results sorted by `ascPrice`.
3. Schedule remaining `total - 10_000` requests sorted by `descPrice`.
4. Collect responses and parse product data.

Here's quick implementation using Python with asynchronous http client package `httpx`:

```python
{! content/examples/discovery-search.py !}
```

Here we used asynchronous python and `httpx` as our http client library to scrape all 13790 products with very few requests just in few minutes!


## Summary and Further Reading

To summarize reverse engineering website's search API is a brilliant scrape target discovery technique however it's more difficult to develop as it requires reverse-engineer effort and all of the code becomes very domain specific.  

{! content/partial/Web Scraping Target Discovery_outro.md !}
