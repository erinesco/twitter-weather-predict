import json
import sys
import codecs

from functools import partial

import random
import math
import copy
from nltk.classify import NaiveBayesClassifier

from sklearn.svm import LinearSVC
from nltk.classify.scikitlearn import SklearnClassifier

def format_observed_weather():
    previous_weather = None
    observed_weather = {}
    for line in open('data/weatherData.json', 'r'):
        line = json.loads(line)
        current_weather, current_time = str(unicode(line['weather'][0]['main'])).replace("'", ""), line['dt']
        if previous_weather != current_weather:
            # Hit a new weather type
            if previous_weather == None:
                observed_weather[current_weather] = []
                observed_weather[current_weather].append([current_time])
            else:
                # Transitioning from one weather type to another
                if current_weather not in observed_weather:
                    observed_weather[current_weather] = []
                observed_weather[current_weather].append([current_time])
                observed_weather[previous_weather][-1].append(current_time)
            previous_weather = current_weather
    #add final time
    observed_weather[previous_weather][-1].append(current_time)
    return observed_weather

def find_tweets_weather(observed_weather):
    tweets_by_weather = {}
    for key, value in observed_weather.iteritems():
        tweets_by_weather[key] = []
    for line in open('data/twitter_data_formated.json', 'r'):
        line = json.loads(line)
        tweet, tweet_time = line['text'], line['timestamp']
        for key, value in observed_weather.iteritems():
            key = str(key)
            for time_range in value:
                if tweet_time > time_range[0] and tweet_time <= time_range[1]:
                    tweets_by_weather[key].append(tweet)
    return tweets_by_weather

def features(sentence):
    words = sentence.lower().split()
    return dict(('contains(%s)' % w, True) for w in words)

def label_data(featureset, label):
    labeled_data = []
    for element in featureset:
        labeled_data.append((element, label))
    return labeled_data

def compute_features(tweets_by_weather):
    clear_featuresets = list(map(features, tweets_by_weather['Clear']))
    cloudy_featuresets = list(map(features, tweets_by_weather['Clouds']))
    rainy_featuresets = list(map(features, tweets_by_weather['Rain']))
    final_data = label_data(clear_featuresets, 'Clear') + label_data(cloudy_featuresets, 'Clouds') + label_data(rainy_featuresets, 'Rain')
    return final_data

def divide_data(final_data, folds):
    data_chunks = []
    data_amount = len(final_data)
    random.shuffle(final_data)
    step_size = int(math.ceil(data_amount/folds))
    remainder = data_amount % folds
    for i in range(0, data_amount, step_size):
        train_data = copy.deepcopy(final_data) #justpythonthings
        if i + step_size == data_amount - remainder:
            test_data = train_data[i:i+step_size+remainder]
            train_data[i:i+step_size+remainder] = []
            data_chunks.append(test_data)
            break
        else:
            test_data = train_data[i:i+step_size]
            train_data[i:i+step_size] = []
        data_chunks.append(test_data)
    return data_chunks

def divide_data_fast(data, folds):
    data_chunks = [[] for i in xrange(folds)]
    random.shuffle(data)
    chunk_size = math.ceil(len(data) / folds)
    chunk_index = 0
    for element in data:
        data_chunks[chunk_index].append(element)
        chunk_index += 1
        if chunk_index >= len(data_chunks):
            chunk_index = 0
    return data_chunks




def cross_validate(data_chunks, learner, training_function_string, classification_function_string):
    
    averages = []
    for i in range(0,len(data_chunks)):
        train_data = []
        correct, total = 0, 0
        train_chunks = data_chunks
        test_chunk = train_chunks[i]
        chunk_count = 0
        for chunk in train_chunks:
            if chunk_count != i:
                for tweet in chunk:
                    train_data.append(tweet)
            chunk_count += 1
        
        print 'Before Attr'
        sys.stdout.flush()
        #classifyMethod = getattr(learner, classification_function_string)
        #trainingMethod = getattr(learner, training_function_string)
        model = SklearnClassifier(LinearSVC(multi_class='crammer_singer'))
        model.train(train_data)
       # model = NaiveBayesClassifier
        #classifier = model.train(train_data)
        print 'Before Train'
        sys.stdout.flush()
        #classifier = trainingMethod(train_data)
        print 'Before test'
        for tweet in test_chunk:
            total += 1
            if tweet[1] == model.classify_many(tweet[0]):#classifyMethod(tweet[0]):#:classifier.classify(tweet[0]):
               correct += 1
        accuracy = float(correct) / float(total)
        averages.append(accuracy)
        print "Fold: " + str(i+1) + ", Accuracy: " + str(accuracy)
    #classifier.show_most_informative_features()
    return sum(averages)/len(averages)

