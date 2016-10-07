# Combine twitter and weather data to produce tweets labeled by weather
import json

tweets = []
previous_weather = None
observed_weather = {}
previous_time = 0
for line in open('data/weatherData.json', 'r'):
    line = json.loads(line)
    current_weather = str(unicode(line['weather'][0]['main'])).replace("'", "")
    current_time = line['dt']
    print current_weather, current_time
    if previous_weather == current_weather:
        # Still in the same type of weather...
        continue
    else:
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

print observed_weather




