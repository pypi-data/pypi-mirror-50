import argparse

from .client import Client


def main():
    parser = argparse.ArgumentParser(
        description="Facebook Developer tool echo")
    parser.add_argument(
        "-c", "--cookie", help="editthiscookie export", required=True)
    parser.add_argument("-u", "--url", help="url", required=True)
    args = parser.parse_args()

    client = Client(args.cookie)
    response = client.get(args.url)

    print(client.unescape(response.text))


if __name__ == "__main__":
    main()
