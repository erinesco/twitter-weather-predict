#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "accesstoken"
access_token_secret = "accesstokensecret"
consumer_key = "consumerkey"
consumer_secret = "consumersecret"


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