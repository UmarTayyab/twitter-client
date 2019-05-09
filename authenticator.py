from tweepy import OAuthHandler
import credentials


class Authenticator():
    def authenticate(self):
        auth = OAuthHandler(credentials.CONSUMER_KEY,
                            credentials.CONSUMER_SECRET)
        auth.set_access_token(credentials.ACCESS_TOKEN,
                              credentials.ACCESS_TOKEN_SECRET)
        return auth
