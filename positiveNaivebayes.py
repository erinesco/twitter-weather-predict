# Combine twitter and weather data to produce tweets labeled by weather
from pnbHelper import *
from nltk.classify import NaiveBayesClassifier
from nltk.classify import PositiveNaiveBayesClassifier


# Get observed weather in formatted time ranges
observed_weather = format_observed_weather()
# Assign tweets to their respective time range and weather
tweets_by_weather = find_tweets_weather(observed_weather)
# Compute features (words) and their labels
final_data = compute_features(tweets_by_weather)
cross_validate(final_data, 5, PositiveNaiveBayesClassifier)
# data_chunks = divide_data(final_data, 5)
# print "AVERAGE ACCURACY: " + str(cross_validate(data_chunks, NaiveBayesClassifier))
