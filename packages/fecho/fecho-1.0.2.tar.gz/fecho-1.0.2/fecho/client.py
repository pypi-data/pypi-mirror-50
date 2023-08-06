import json

import requests

from .exceptions import InvalidCookie

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

    def get(self, url, **kwargs):
        if kwargs.get("params"):
            url += "?" + requests.compat.urlencode(kwargs.get("params"))
            kwargs.pop("params")

        escaped_url = requests.compat.quote_plus(url)
        response = requests.get('https://developers.facebook.com/tools/debug/echo/?q=%s' %
                                escaped_url, headers=self.headers, **kwargs)
        return response
