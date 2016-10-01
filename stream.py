#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "333824526-Mbcqo0jLcCykFVKJNX9yztNcts6WonmbARvsC19v"
access_token_secret = "tD9iBpnWF5WvqMFzYsTpQlv8wlYaogrvVsqfmJ0GK09VT"
consumer_key = "euRoqSWyzz3FpHHbsV1DIOG09"
consumer_secret = "mMFNYUg2LDhAWqh4OnOsEBLFHkPnreop6Mi7O3WU2CAD7Y59Vy"


filewrite = 'data/twitter_data.txt'
datafile = open(filewrite, 'w')

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data['location']
        #datafile.write(data)
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #Streaming API location currently San Fransisco
    stream.filter(locations=[-122.75,36.8,-121.75,37.8])