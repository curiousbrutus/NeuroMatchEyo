"""
Task 1.2, 1.3

Filtering URLs from HTML
"""

from __future__ import annotations

import re
from urllib.parse import urljoin, urlparse

def find_urls(html: str, base_url: str = "https://en.wikipedia.org") -> set[str]:
    """
    Find all URLs in an HTML string.

    Args:
        html (str): The HTML string to search for URLs.
        base_url (str, optional): The base URL to use for relative URLs.

    Returns:
        urls (set[str]): A set of all URLs found in the HTML string.
    """
    href_pat = re.compile(r'<a.+?href="([^"]+)"', flags=re.IGNORECASE)
    intern_pat = re.compile(r'#[\w-]+', flags=re.IGNORECASE)

    urls = set()
    def_pat = re.compile(r'^//', flags=re.IGNORECASE)
    for href in href_pat.findall(html):
        if href.startswith("#"):
            continue

        if not def_pat.search(href) and href.startswith("/"):
            href = re.sub(intern_pat, "", href)
            urls.add(urljoin(base_url, href))
        elif href.startswith("//"):
            href = re.sub(intern_pat, "", href)
            urls.add("https:" + href)
        else:
            href = re.sub(intern_pat, "", href)
            urls.add(href)

    return urls

def find_articles(html: str, output: str = None, base_url: str = "https://en.wikipedia.org") -> set[str]:
    """
    Find all the article links on a Wikipedia page

    Args:
        html (str): the HTML content of the Wikipedia page
        output (Optional[str]): file to write to if wanted
        base_url (str, optional): the base URL of the page

    Returns:
        articles (set[str]): set of article links found on the page
    """
    urls = find_urls(html, base_url=base_url)

    # Filter out non-article links
    articles = set()

    for url in urls:
        # Check if the URL points to a Wikipedia article
        if re.match(r'https://\w{2}\.wikipedia\.org/wiki/[^:]+$', url, re.IGNORECASE):
            articles.add(url)

    # Write to file if requested
    if output:
        with open(output, "w") as f:
            f.write("\n".join(articles))

    return articles





## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attribute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set
