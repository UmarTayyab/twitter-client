import re
import pandas as pd
import numpy as np
from textblob import TextBlob
from nltk import word_tokenize


class TweetsClassifer():

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        polarity = analysis.sentiment.polarity
        if polarity > 0:  # Positive
            return 1
        elif polarity == 0:  # Neutral
            return 0
        else:  # Negative
            return -1

    def thoughts_about(self, topic, tweets):
        topic_lower = topic.lower()
        topic_title = topic.title()
        df = self.to_data_frame(tweets)
        tokens = df.tweet.map(word_tokenize)
        return df.loc[tokens.map(lambda tweets: topic_lower in tweets or topic_title in tweets).values]

    def to_data_frame(self, tweets):
        # Create lists to hold each variable
        ids, tweetsList, length, created_at, favorites, retweets = [], [], [], [], [], []

        # Loop over tweets and append data to respective lists
        for tweet in tweets:
            ids.append(tweet.id_str)
            tweetsList.append(tweet.text)
            length.append(len(tweet.text))
            created_at.append(tweet.created_at)
            favorites.append(tweet.favorite_count)
            retweets.append(tweet.retweet_count)

        # Create a Pandas Dataframe from lists populated above
        df = pd.DataFrame({'id': ids, 'tweet': tweetsList, 'length': length,
                           'created_at': created_at, 'favorites': favorites, 'retweets': retweets})

        return df
