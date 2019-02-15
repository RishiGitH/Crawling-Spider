# -*- coding: utf-8 -*-
# filename: crawler.py
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import sqlite3  
from html.parser import HTMLParser 
from urllib.parse import urlparse
from sys import getrecursionlimit, setrecursionlimit
setrecursionlimit(1500)



class HREFParser(HTMLParser):  
    hrefs = set()
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            dict_attrs = dict(attrs)
            if dict_attrs.get('href'):
                self.hrefs.add(dict_attrs['href'])


def get_local_links(html, domain):  
    hrefs = set()
    parser = HREFParser()
    parser.feed(html)
    for href in parser.hrefs:
        u_parse = urlparse(href)
        if href.startswith('/'):
            hrefs.add(u_parse.path)
        else:
          if u_parse.netloc == domain:
            hrefs.add(u_parse.path)
    return hrefs


class CrawlerCache(object):  
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS sites
            (domain text, url text, content text)''')
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def set(self, domain, url, data):
        self.cursor.execute("INSERT INTO sites VALUES (?,?,?)",
            (domain, url, data))
        self.conn.commit()

    def get(self, domain, url):
        self.cursor.execute("SELECT content FROM sites WHERE domain=? and url=?",
            (domain, url))
        row = self.cursor.fetchone()
        if row:
            return row[0]

    def get_urls(self, domain):
        self.cursor.execute("SELECT url FROM sites WHERE domain=?", (domain,))
        return [row[0] for row in self.cursor.fetchall()]


class Crawler(object):  
    def __init__(self, cache=None, depth=1500):
        self.depth = depth
        self.content = {}
        self.cache = cache

    def crawl(self, url, no_cache=None):
        u_parse = urlparse(url)
        self.domain = u_parse.netloc
        self.content[self.domain] = {}
        self.scheme = u_parse.scheme
        self.no_cache = no_cache
        self._crawl([u_parse.path], self.depth)

    def set(self, url, html):
        self.content[self.domain][url] = html
        if self.is_cacheable(url):
            self.cache.set(self.domain, url, html)

    def get(self, url):
        page = None
        if self.is_cacheable(url):
          page = self.cache.get(self.domain, url)
        if page is None:
          page = self.curl(url)
        else:
          print("cached url... [%s] %s" % (self.domain, url))
        return page

    def is_cacheable(self, url):
        return self.cache and self.no_cache \
            and not self.no_cache(url)

    def _crawl(self, urls, max_depth):
        n_urls = set()
        if max_depth:
            for url in urls:
                if url not in self.content:
                    html = self.get(url)
                    self.set(url, html)
                    n_urls = n_urls.union(get_local_links(html, self.domain))
            self._crawl(n_urls, max_depth-1)

    def curl(self, url):
        try:
            print("retrieving url... [%s] %s" % (self.domain, url))
            req = urllib2.Request('%s://%s%s' % (self.scheme, self.domain, url))
            response = urllib2.urlopen(req)
            return response.read().decode('ascii', 'ignore')
        except urllib2.HTTPError as e:
            print("error [%s] %s: " % (self.domain, url))
            return ''