import json

import requests

from .exceptions import InvalidCookie, InvalidURL

try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

IMPORTANT_COOKIES = [
    "c_user",
    "datr",
    "fr",
    "presence",
    "xs"
]


def format_cookie(cookie_dough):
    """editthiscookie import"""
    try:
        cookie = json.loads(cookie_dough)
        simple_cookie = [c.get("name") + "=" + c.get("value")
                         for c in cookie if c.get("name") in IMPORTANT_COOKIES]
        return "; ".join(simple_cookie)
    except Exception as e:
        raise InvalidCookie(e)


def handle_response(response):
    """handles responses"""
    # print(response.status_code)
    # print(response.url)
    # print(response.headers)
    if response.status_code == 404 and "https://www.facebook.com/login.php?next=" in response.url:
        raise InvalidCookie("Facebook redirected to login.php")
    if response.status_code == 200 and response.text.strip().endswith("The document returned no data."):
        raise ReturnedNoData()


class Client(object):
    def __init__(self, cookie):
        self.cookie = format_cookie(cookie)
        self.headers = {
            'Host': 'developers.facebook.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'deflate',
            'Connection': 'keep-alive',
            'Cookie': self.cookie,
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers'
        }
        self.html_parser = HTMLParser()

    def unescape(self, html):
        return self.html_parser.unescape(html)

    def get(self, url, **kwargs):
        if kwargs.get("params"):
            url += "?" + requests.compat.urlencode(kwargs.get("params"))
            kwargs.pop("params")

        parsed_url = requests.compat.urlparse(url)
        if not parsed_url.scheme:
            parsed_url._replace(**{"scheme": "http"})
        if not parsed_url.path:
            parsed_url._replace(**{"path": "/"})
        if not parsed_url.netloc:
            raise InvalidURL(parsed_url.geturl())

        escaped_url = requests.compat.quote_plus(parsed_url.geturl())
        response = requests.get('https://developers.facebook.com/tools/debug/echo/?q=%s' %
                                escaped_url, headers=self.headers, **kwargs)
        handle_response(response)
        return response
