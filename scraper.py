from sys import argv
from twitter_client import Client


def main(username, limit, include_rts, ignore_replies, export, file_format):
    print("\t\t\t Initiating Scraper for {}".format(username))

    client = Client()

    filename = client.scrape_tweets(
        username=username, limit=limit, include_rts=include_rts, exclude_replies=ignore_replies, save_to_file=True, file_format='csv')

    print(filename)


if __name__ == "__main__":
    if len(argv) == 1:
        print("Usage: python scraper.py username limit? include_rts? ignore_replies? save_to_file? file_format")
    else:
        username = argv[1]
        limit = argv[2] if argv[2] else 100
        rts = argv[3] if argv[3] else True
        no_replies = argv[4] if argv[4] else True
        save = argv[5] if argv[5] else False
        file_format = 'csv'
        main(username, limit, rts, no_replies, save, file_format)
