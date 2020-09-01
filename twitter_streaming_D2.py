from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re

access_token = "1264474938892640259-vZoeYKh9hRmgQGcMLIWvmY79hfkKZQ"
access_token_secret = "10JTkjx6teD8HZUIk1JHQY0i2ZxpUHx5UnSdOlhFh1og8"
consumer_key = "i1h02pEpD5nWz6xSfLrmgAkqf"
consumer_secret = "dle16fYGKzGQQvVJVfgll169SMD36VZeDRMszyDPTDJdD95Dvh"

tracklist = ['#COVID-19']

tweet_count = 0

n_tweets = 1000
f = open("D2.csv", "w")
f.close() 

# class to handle tweet stream
class StdOutListener(StreamListener):
    def on_data(self, data):
        global tweet_count
        global n_tweets
        global stream
        # tweet = {}
        if tweet_count < n_tweets:
            try:
                print(tweet_count, data, "\n")
                tweet_data = json.loads(data)
                pattern1 = re.compile(r'\n')
                tweet_txt = pattern1.sub(r'', tweet_data["retweeted_status"]["extended_tweet"]["full_text"])
                pattern2 = re.compile(r'RT')
                tweet = pattern2.sub(r'', tweet_txt)
                f = open("D2.csv", "a+")
                f.write(str(tweet_data['id']) + ",\"" + tweet + "\"\n")
                tweet_count += 1

            except BaseException:
                print("Error:", tweet_count, data)
                try:
                    print(tweet_count, data, "\n")
                    tweet_data = json.loads(data)
                    pattern1 = re.compile(r'\n')
                    tweet_txt = pattern1.sub(r'', tweet_data["extended_tweet"]["full_text"])
                    pattern2 = re.compile(r'RT')
                    tweet = pattern2.sub(r'', tweet_txt)
                    f = open("D2.csv", "a+")
                    f.write(str(tweet_data['id']) + ",\"" + tweet + "\"\n")
                    tweet_count += 1

                except BaseException:
                    print(tweet_count, data, "\n")
                    tweet_data = json.loads(data)
                    pattern1 = re.compile(r'\n')
                    tweet_txt = pattern1.sub(r'', tweet_data["text"])
                    pattern2 = re.compile(r'RT')
                    tweet = pattern2.sub(r'', tweet_txt)
                    f = open("D2.csv", "a+")
                    f.write(str(tweet_data['id']) + ",\"" + tweet + "\"\n")
                    tweet_count += 1

            return True
        else:
            stream.disconnect()
        
    def on_error(self, status):
        print(status)

# handles twitter authentification and the connection to twitter streaming api
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

stream.filter(track = tracklist, languages = ['en'], encoding = 'utf8')