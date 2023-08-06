from http import cookiejar
from urllib.parse import urlparse, parse_qs
import threading
import requests
import bs4 as _bs4
import os
import itertools
import time
import sys
import argparse
import cachelib

import pygments
import pygments.lexers
import pygments.formatters.terminal

CACHE_DIR  = os.environ.get("HOME")
for dir in (".cache", "howcode"):
    CACHE_DIR = os.path.join(CACHE_DIR, dir)
    if not os.path.isdir(CACHE_DIR):
        os.mkdir(CACHE_DIR)
CACHE_ENTRY_MAX = 128

cache = cachelib.FileSystemCache(CACHE_DIR, CACHE_ENTRY_MAX, default_timeout=0)

def formatter(tags, source):
    lexer = None
    for tag in tags:
        try:
            lexer = pygments.lexers.get_lexer_by_name(tag)
            break
        except Exception:
            pass
    if not lexer:
        try:
            lexer = pygments.lexers.guess_lexer(source)
        except Exception:
            return source
    if lexer:
        return pygments.highlight(source, lexer,
          pygments.formatters.terminal.TerminalFormatter(bg='dark'))
    return source

class Thread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return

class Utils:
    @classmethod
    def bs4(self, html, features="html.parser"):
        return _bs4.BeautifulSoup(html, features)

    @classmethod
    def print_and_exit(self, s):
        print("\r> %s    " % s, end="")
        sys.exit()

class Google:
    def __init__(self):
        self.URL_HOME= "https://www.google.com"
        self.URL_SEARCH= "https://www.google.com/search?q={0}&hl=en"

        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
        }
        self.session.cookies = cookiejar.LWPCookieJar()

    def getCookies(self):
        self.session.get(self.URL_HOME, verify=True)

    def SearchLink(self, q):
        _html = self.session.get(self.URL_SEARCH.format(q)).text
        soup = Utils.bs4(_html)
        anchors = self._anchors(soup)

        for a in anchors:
            href = a.get("href")
            link = self._filter_url(href)
            if link:
                return link

    def _anchors(self, soup):
        try:
            return soup.find(id='search').findAll('a')
        except AttributeError:
            gbar = soup.find(id='gbar')
            if gbar:
                gbar.clear()
            return soup.findAll('a')

    def _filter_url(self, link):
        if not link:
            return False
        o = urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc:
            return link
        if link.startswith('/url?'):
            link = parse_qs(o.query)['q'][0]
            o = urlparse(link, 'http')
            if o.netloc and 'google' not in o.netloc:
                return link
        return False

    def close(self):
        self.session.close()

class StackOverFlow:
    def __init__(self):
        self.query = "site:stackoverflow.com%20{0}"
        self.google = Google()
        self.google.getCookies()
        self.session = self.google.session

    def search(self, q):
        links = self.google.SearchLink(self.query.format(q))
        return links

    def code(self, url):
        if not url:
            return '> no answer given'

        link = url + '?answertab=votes'

        code = cache.get(link)
        if arg.cache and code:
            return code

        chtml = self.session.get(link).text
        soup = Utils.bs4(chtml)
        self.tags = self._getTags(soup)
        code = self._getCode(soup).splitlines()

        if len(code[0]) < 20:
            code[0] = "{0:<20}".format(code[0])

        return "> " + "\n> ".join(code)

    def _getCode(self, soup):
        acceptedAnswer = soup.find("div", {"itemprop": "acceptedAnswer"})
        if acceptedAnswer:
            code = acceptedAnswer.findAll("pre")
            if code:
                return "\n".join(map(lambda x: x.text, code))

        answers = soup.findAll("div", {"class": "answer"})
        for a in answers:
            pos = a.find("div", {"class": "post-text"})
            code = pos.findAll("pre")
            if code:
                return "\n".join(map(lambda x: x.text, code))

        return 'no answer given'

    def _getTags(self, soup):
        return map(lambda x: x.text, soup.findAll("a", {"class": "post-tag"}))

def clear_cache():
    is_ok = cache.clear()
    if is_ok:
        print('[+] Cache cleared successfully')
    else:
        print('[+] Clearing cache failed!!')

def _search_wrapper(q):
    ch = StackOverFlow()
    link = ch.search(q)
    if arg.link:
        return "> " + link

    code = ch.code(link)
    if not arg.no_color:
        code = formatter(ch.tags, code)
    cache.set(link, code)

    return code

def _search_with_anim(q):
    f = Thread(target=_search_wrapper, args=(q,))
    f.start()

    # animate
    for i in itertools.cycle("-\|/"):
        if not f.is_alive():
            break
        print("\r[+] searching %s     " % i, end="")
        time.sleep(0.1)
    result_code = f.join()
    if result_code:
        return "\r" + result_code[:-1]

def cli():
    global arg

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('query', metavar='question', type=str, nargs='+',
                        help='the question to answer')
    parser.add_argument('-l', '--link', help='display only the answer link',
                        action='store_true')
    parser.add_argument('--no-color', help='disabled colorized output',
                        action='store_true')
    parser.add_argument("--no-cache", dest="cache", help="don't use cache file",
                        action="store_false")
    parser.add_argument('-C', '--clear-cache', help='clear the cache',
                        action='store_true')
    arg = parser.parse_args()

    if arg.clear_cache:
        clear_cache()
    elif arg.query:
        arg.query = " ".join(arg.query)
        print(_search_with_anim(arg.query))
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()
