import re
from typing import List

import requests
from parsel import Selector


def parse_sitemap(url: str) -> List[str]:
    """scrape sitemap and item urls from a sitemap link"""
    print(f"scraping: {url}")
    resp = requests.get(url)
    # turn html text to a parsable tree object
    doc_tree = Selector(resp.text)
    # find all <sitemap> nodes and take their urls
    other_sitemaps = doc_tree.xpath("//sitemap/text()").getall()
    # find all <loc> nodes and take their text (which is an url)
    urls = doc_tree.xpath("//loc/text()").getall()
    return other_sitemaps + urls


product_urls = set()
sitemap_directory = "https://us.shein.com/sitemap-index.xml"
for url in parse_sitemap(sitemap_directory):
    if "-products-" not in url:
        continue
    for url in parse_sitemap(url):
        # product urls match pattern com/<some product naming>.html
        # skip non-product urls
        if not re.search(r"shein.com/.+?\.html", url):
            continue
        product_urls.add(url)
# print("\n".join(product_urls[-100:]))
print(len(product_urls))
