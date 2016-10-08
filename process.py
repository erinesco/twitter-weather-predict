# Combine twitter and weather data to produce tweets labeled by weather
import json
from nltk.classify import NaiveBayesClassifier
from functools import partial

tweets = []
previous_weather = None
observed_weather = {}
previous_time = 0
for line in open('data/weatherData.json', 'r'):
    line = json.loads(line)
    current_weather = str(unicode(line['weather'][0]['main'])).replace("'", "")
    current_time = line['dt']
    if previous_weather != current_weather:
        # Hit a new weather type
        if previous_weather == None:
            # If this is the first weather instance we have seen
            observed_weather[current_weather] = []
            observed_weather[current_weather].append([current_time])
        else:
            # Transitioning from one weather type to another
            if current_weather in observed_weather:
                # if we have seen this weather type before
                observed_weather[current_weather].append([current_time])
                observed_weather[previous_weather][-1].append(current_time)
            else:
                observed_weather[current_weather] = []
                observed_weather[current_weather].append([current_time])
                observed_weather[previous_weather][-1].append(current_time)
        previous_weather = current_weather
        previous_time = current_time

#add final time
observed_weather[previous_weather][-1].append(current_time)

tweets_by_weather = {}
#### Look at twitter data
for key, value in observed_weather.iteritems():
    tweets_by_weather[key] = []

for line in open('data/twitter_data_formated.json', 'r'):
    line = json.loads(line)
    tweet = line['text']
    tweet_time = line['timestamp']
    for key, value in observed_weather.iteritems():
        key = str(key)
        for time_range in value:
            if tweet_time > time_range[0] and tweet_time <= time_range[1]:
                tweets_by_weather[key].append(tweet)

def features(sentence,):
    words = sentence.lower().split()
    return dict(('contains(%s)' % w, True) for w in words)


clear_featuresets = list(map(features, tweets_by_weather['Clear']))
cloudy_featuresets = list(map(features, tweets_by_weather['Clouds']))

new_clear, new_cloudy = [], []
for element in clear_featuresets:
    new_clear.append((element, 'Clear'))
for element in cloudy_featuresets:
    new_cloudy.append((element, 'Cloudy'))

final_data = new_clear + new_cloudy

classifier = NaiveBayesClassifier.train(final_data)
classifier.show_most_informative_features()

