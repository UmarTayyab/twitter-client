from tweepy.streaming import StreamListener
from random import randint
from twitter_client import Client
import re

# For analysis
import csv
import pandas as pd
from textblob import TextBlob
from nltk import word_tokenize


class BaseListener(StreamListener):

    def __init__(self, tweets_filename, username):
        self.tweets_filename = tweets_filename
        self.username = username
        self.api = Client().get_client_api()

        self.dataset = read_as_df("boredelonmusk.csv")
        self.regex = "#\w+\S"

    def on_status(self, status):
        try:
            self.print_tweet(status.text)
            self.respond_back(status)
            return True
        except BaseException as e:
            print('Error on_data: {}'.format(e))
        return True

    def on_error(self, status_code):
        # Returns false on data_method if rate limit
        if status_code == 420:
            print('An error occurred: {}'.format(status_code))
        return False

    def print_tweet(self, tweet):
        print(tweet)

    def save_to_file(self, tweet):
        with open(self.tweets_filename, 'a') as f:
            f.write(tweet)

    def respond_back(self, tweet):
        user = tweet.user  # user object
        # if (user.screen_name != self.username):
        if True:
            print('Processing tweet and retweeting.')
            tweet_url = 'https://twitter.com/{}/status/{}'.format(
                user.screen_name, tweet.id_str)  # url of origin tweet

            thoughts = re.sub("#", "", re.search(
                self.regex, tweet.text).group())

            text = thoughts_about(thoughts, self.dataset).text.values.tolist()

            # Only one result returned
            if len(text) == 1:
                to_tweet = '{t} {url}'.format(t=text[0], url=tweet_url)

            # Multiple results. Return 1 at random
            elif len(text) > 1:
                index = randint(1, len(text))
                to_tweet = '{t} {url}'.format(t=text[index-1], url=tweet_url)

            # No results
            else:
                text = thoughts_about(
                    "space", self.dataset).text.values.tolist()
                index = randint(1, len(text))
                to_tweet = '{t} {url}'.format(t=text[index-1], url=tweet_url)

            # self.api.update_with_media(filename, to_tweet)
            self.api.update_status(to_tweet)


def read_as_df(filename):
    ids = []  # 0
    created_at = []  # 1
    tweets = []  # 2

    with open(filename) as f:
        _file = csv.reader(f, delimiter=',')
        for row in _file:
            try:
                ids.append(row[0])
                created_at.append(row[1])
                tweets.append(row[2])
            except (NameError, KeyError):
                pass

    df = pd.DataFrame({'id': ids, 'created_at': created_at, 'text': tweets})
    return df


def thoughts_about(topic, tweets):
    topic_lower = topic.lower()
    topic_title = topic.title()
    tokens = tweets.text.map(word_tokenize)
    return tweets.loc[tokens.map(lambda tweets: topic_lower in tweets or topic_title in tweets).values]
