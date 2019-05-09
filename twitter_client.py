from tweepy import API, Cursor
from authenticator import Authenticator
import csv


class Client():
    def __init__(self, user=None):
        self.auth = Authenticator().authenticate()
        self.client = API(self.auth)
        self.user = user

    def get_client_api(self):
        return self.client

    def get_timeline_tweets(self, limit):
        tweets = []
        for tweet in Cursor(self.client.user_timeline, id=self.user).items(limit):
            tweets.append(tweet)
        return tweets

    def get_friends_list(self, limit):
        friends = []
        for friend in Cursor(self.client.friends, id=self.user).items(limit):
            friends.append(friend)
        return friends

    def get_news_timeline(self, limit):
        tweets = []
        for tweet in Cursor(self.client.home_timeline, id=self.user).items(limit):
            tweets.append(tweet)
        return tweets

    def post_tweet(self, tweet):
        self.client.update_status(tweet)

    def post_tweet_with_media(self, tweet, filename, file=None):
        if file is not None:
            self.client.update_with_media(filename, tweet, file)
        else:
            self.client.update_with_media(filename, tweet)

    def retweet(self, tweetId):
        self.client.retweet(tweetId)
        print('Retweeted successfully.')

    def scrape_tweets(self, username, limit=100, include_rts=True, exclude_replies=True, save_to_file=False, file_format='csv'):
        all_tweets = []  # empty list to hold all scraped tweets

        # user timeline for user: username from whom
        # the tweets need to be extracted
        tweets = self.client.user_timeline(
            screen_name=username, count=limit, include_rts=include_rts, exclude_replies=exclude_replies)

        all_tweets.extend(tweets)

        # id of oldest tweet would be end of the list: all_tweets - 1
        oldest_tweet = all_tweets[-1].id - 1

        # Loop to scrape tweets until none are left
        while len(tweets):
            # max-id used to define oldest tweet to avoid
            # appending duplicated tweets to list: all_tweets
            tweets = self.client.user_timeline(
                screen_name=username, count=limit, include_rts=include_rts, exclude_replies=exclude_replies, max_id=oldest_tweet)

            # extend list:all_tweets with fetched tweets
            all_tweets.extend(tweets)

            # update id for oldest tweet
            oldest_tweet = all_tweets[-1].id - 1

            print('...{} tweets have been scraped so far.'.format(len(all_tweets)))
        print('Scraping complete. Total tweets scraped: {}'.format(len(all_tweets)))

        # Save tweets to a file (format defaults to csv) and
        # returns filename
        if save_to_file is True:
            filename = '{file_name}.{file_format}'.format(
                file_name=username, file_format=file_format)
            self.save_to_file(all_tweets, filename, file_format)
            return filename
        else:
            return all_tweets  # return list containg all scraped tweets

    def save_to_file(self, tweets, filename='output', format='csv'):

        output = [[tweet.id_str, tweet.created_at, tweet.text, tweet.source, tweet.in_reply_to_status_id_str if tweet.in_reply_to_status_id_str else None, tweet.in_reply_to_user_id_str if tweet.in_reply_to_user_id_str else None,
                   tweet.in_reply_to_screen_name if tweet.in_reply_to_screen_name else None, tweet.user, tweet.coordinates, tweet.place, tweet.is_quote_status if tweet.is_quote_status else None, tweet.retweet_count, tweet.favorite_count, tweet.entities, tweet.lang] for tweet in tweets]
        headers = ['id', 'created_at', 'text', 'source', 'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name',
                   'user', 'coordinates', 'place', 'is_quote_status', 'retweet_count', 'favorite_count', 'entities', 'lang']
        if format.lower() == 'csv':
            with open(filename, 'w') as out:
                writer = csv.writer(out, delimiter=',')
                writer.writerow(headers)
                writer.writerows(output)
            return filename
        else:
            pass

    def save_media_links(self, tweets, username):
        output = []
        headers = ['id', 'created_at', 'text', 'media']

        for tweet in tweets:
            try:
                print(tweet.entities['media'][0]['media_url_https'])
            except (NameError, KeyError):
                print('No media included in tweet.')
            else:
                output.append([tweet.id_str, tweet.created_at, tweet.text,
                               tweet.entities['media'][0]['media_url_https']])

        with open('{}-media.csv'.format(username), 'w') as out:
            writer = csv.writer(out)
            writer.writerow(headers)
            writer.writerows(output)
        return '{}-media.csv'.format(username)
