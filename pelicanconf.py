#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = "Bernardas Ališauskas"
SITENAME = "Scrapecrow"
SITEURL = ""
SITE_LOGO = "/images/logo.svg"

PATH = "content"

TIMEZONE = "Europe/Paris"

DEFAULT_LANG = "en"
# Theming
THEME = "dotrocks"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
AUTHOR_IMG = "images/author.jpg"
AUTHOR_WEB = "http://granitosaurus.rocks"

# Social widget
SOCIAL = (
    ("You can add links in your config file", "#"),
    ("Another social link", "#"),
)

DEFAULT_PAGINATION = 10
DEFAULT_CATEGORY = "articles"

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
SITETITLE = AUTHOR
SITEURL = "http://localhost:8000"
SITESUBTITLE = (
    "Python programmer and a goof who loves free software, video-games and heavy metal"
)
SITEDESCRIPTION = "Thoughts and Writings of Granitosaurus"
SITELOGO = SITEURL + "/images/core/granitosaurus.png"
FAVICON = SITEURL + "/images/favicon.ico"

# Main menu
MAIN_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
DISPLAY_RSS_ON_MENU = True
MENUITEMS = (
    ("about", "/pages/about.html"),
    ("hire", "/pages/hire.html"),
    ("#web-scraping on matrix", "https://matrix.to/#/#web-scraping:matrix.org"),
)
FOOTERITEMS = (
    ("Archives", "/archives.html"),
    ("Tags", "/tags.html"),
)
SOCIAL = (
    ("github", "https://github.com/granitosaurus"),
    ("mastodon", "https://mastodon.host/@wraptile"),
    ("at", "mailto:bernard@scrapecrow.com"),
    ("matrix-org", "https://matrix.to/#/#web-scraping:matrix.org"),
    ("rss-square", "/atom.xml"),
)


# Feed generation is usually not desired when developing
THEME = "dotrocks"

# Social widget
DEFAULT_PAGINATION = 20

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike",
    "version": "4.0",
    "slug": "by-sa",
}
COPYRIGHT_YEAR = 2021
STATIC_PATHS = ["images", "pages", "data", "extra/CNAME", "gifs"]

# CNAME fix
EXTRA_PATH_METADATA = {
    "extra/CNAME": {"path": "CNAME"},
    "images/favicon.ico": {"path": "favicon.ico"},
}

# feed
FEED_DOMAIN = SITENAME
FEED_ATOM = "atom.xml"
FEED_RSS = "rss.xml"


# Plugins and their settings
PLUGIN_PATHS = ["../pelican-plugins"]
PLUGINS = ["shortcodes", "pelican-toc"]
SHORTCODES = {
    "image": """<a href="/images/{{src}}"><img src="/images/{{src}}" title="{{desc}}"></img></a><figcaption>{{desc}}</figcatpion>""",
    "mp4gif": """<video width="480" height="240" autoplay loop muted title="{{desc}}"><source src="/gifs/{{src}}" type="video/mp4"></video><figcaption>{{desc}}</figcation>""",
}
TOC = {
    "TOC_HEADERS": "^h[1-6]",
    "TOC_INCLUDE_TITLE": "false",
}
