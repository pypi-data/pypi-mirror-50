import argparse

from .client import Client
from .utils import decode_html

try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser


def main():
    parser = argparse.ArgumentParser(
        description="Facebook Developer tool echo")
    parser.add_argument(
        "-c", "--cookie", help="editthiscookie export", required=True)
    parser.add_argument("-u", "--url", help="url", required=True)
    args = parser.parse_args()

    client = Client(args.cookie)
    response = client.get(args.url)

    html_parser = HTMLParser()
    print(html_parser.unescape(response.text))


if __name__ == "__main__":
    main()
