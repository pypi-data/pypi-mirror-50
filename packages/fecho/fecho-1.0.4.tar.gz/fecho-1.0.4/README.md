# fecho [![Build Status](https://travis-ci.com/thehappydinoa/fecho.svg?branch=master)](https://travis-ci.com/thehappydinoa/fecho)

Uses Facebook's debugging tool to bypass CAPTCHA and other blacklists.

## Install

```bash
pip install fecho
```

## Usage

The cookie can be extracted using the [EditThisCookie](http://www.editthiscookie.com/blog/2014/03/install-editthiscookie/) browser extension. Just export the cookies after logging into [Facebook](https://www.facebook.com/).

### Command Line

```bash
fecho --url 'https://www.google.com/search?q=sample+query' --cookie '[
{
    "domain": ".facebook.com",
    "expirationDate": 1597023793.932123,
    "hostOnly": false,
    "httpOnly": false,
    "name": "c_user",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "",
    "id": 1
},
...
]'
```

### Python

```python
from fecho import Client

COOKIE = """
[
{
    "domain": ".facebook.com",
    "expirationDate": 1597023793.932123,
    "hostOnly": false,
    "httpOnly": false,
    "name": "c_user",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "",
    "id": 1
},
...
]
"""

client = Client(COOKIE)

response = client.get("https://www.google.com/search?q=test")

print(client.unescape(response.text))
```

## Note

This project was inspired by [s0md3v/goop](https://github.com/s0md3v/goop)
