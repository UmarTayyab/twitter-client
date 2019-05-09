from tweets_streamer import Streamer
from textblob import TextBlob
from nltk import word_tokenize
import re
import pandas as pd
import csv
from sys import argv
from random import randint


def bot():
    tracking_list = ['@umarr_t']
    filename = 'ElonMusk.json'
    """
    Twitter Bot
    @param filename: specify filename to save data to
    @param tracking_list: list of keywords(usernames, hashtags, topics) to track
    @param username: authenticated user's screen name

    Creates a streamer object that streams tweets in real-time via twitter api - it
    listens for tweets w.r.t keywords in tracking_list and Retweets with a random Elon Musk
    meme alongwith mentioning the origin tweet.
    """
    streamer = Streamer()
    streamer.stream(filename, tracking_list, 'umarr_t')


def thoughts_about(topic, tweets):
    topic_lower = topic.lower()
    topic_title = topic.title()
    tokens = tweets.text.map(word_tokenize)
    return tweets.loc[tokens.map(lambda tweets: topic_lower in tweets or topic_title in tweets).values]


def clean_tweet(self, tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


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


if __name__ == "__main__":
    # filename = argv[1]
    # tweets = read_as_df(filename)
    # thoughts = argv[2]

    # # String starts with # to get the hashtag
    # # String contains 1+ alphanumeric characters
    # # String ends right before a space
    # regex = "#\w+\S"

    # t = thoughts_about(thoughts, tweets).text.values.tolist()

    # if len(t) > 1:
    #     index = randint(1, len(t))
    #     print(t[index-1])
    # else:
    #     t = thoughts_about('Space', tweets).text.values.tolist()
    #     index = randint(1, len(t))
    #     print(t[index-1])
    # print(t[0])
    bot()
