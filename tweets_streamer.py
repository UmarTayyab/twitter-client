from tweets_listener import BaseListener
from authenticator import Authenticator
from twitter_client import Client
from tweepy import Stream


class Streamer():

    def __init__(self):
        self.auth = Authenticator().authenticate()

    def stream(self, tweets_filename, tracking_list, username):
        listener = BaseListener(tweets_filename, username)
        stream = Stream(self.auth, listener)
        stream.filter(track=tracking_list)
