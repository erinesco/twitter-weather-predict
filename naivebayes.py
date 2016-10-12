# Combine twitter and weather data to produce tweets labeled by weather
from helper import *
import time

start_time = time.time()

# Get observed weather in formatted time ranges
observed_weather = format_observed_weather()
# Assign tweets to their respective time range and weather
tweets_by_weather = find_tweets_weather(observed_weather)
# Compute features (words) and their labels
final_data = compute_features(tweets_by_weather)
data_chunks = divide_data(final_data, 9)
print "AVERAGE ACCURACY: " + str(cross_validate(data_chunks))
print "TIME ELAPSED: " + str(time.time() - start_time)

