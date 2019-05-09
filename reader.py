import csv


def main():
    filename = "elonmusk.csv"
    output = []
    with open(filename) as f:
        tweets = csv.reader(f, delimiter=',')
        headers = ['id', 'created_at', 'text', 'media']
        for tweet in tweets:
            try:
                tweet[-2] = eval(tweet[-2])

                output.append([tweet[0], tweet[1], tweet[2], tweet[-2]
                               ['media'][0]['media_url_https']])
            except (NameError, KeyError):
                pass

    with open('{}-media.csv'.format(filename), 'w') as out:
        writer = csv.writer(out)
        writer.writerow(headers)
        writer.writerows(output)
    print('{total} images/videos have been scraped. Exported to file: {file}'.format(
        total=len(output), file='{}-media.csv'.format(filename)))
    return '{}-media.csv'.format(filename)


if __name__ == "__main__":
    main()
