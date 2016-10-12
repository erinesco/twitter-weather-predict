#Import the necessary methods
import simplejson as json
import io
import re
import sys
import codecs
import time

# filewrite = 'data/twitter_data.txt'
# datafile = open(filewrite, 'w')

#This is a basic listener that just prints received tweets to stdout.
class NoviceLearner():

    def __init__(self):
        self.catagories = {
          "thunderstorms" : {
                "thunder" : "thunder",
                "thunderstorms" : "thunderstorms",
                "thunderstorm" : "thunderstorm",
                "storm" : "storm",
                "lighting" : "lighting",
                "high wind" : "high wind"
            },
            "drizzle": {
                "drizzle" : "drizzle",
                "droplets" : "droplets",
                "sprinkle" : "sprinkle",
                "wet out" : "wet out",
                "light rain" : "light rain",
                "cloudy" : "cloudy",
            },
            "rain" : {
                "rain" : "rain",
                "rainy" : "rainy",
                "wet" : "wet",
                "soaked" : "soaked",
                "drive slow" : "snow",
                "wet roads" : "wet roads"
            },
            "snow" : {
                "snow" : "snow",
                "snowflakes" : "snowflakes",
                "sleding" : "sleding",
                "salting roads" : "salting roads",
                "shoveling" : "shoveling",
                "snowblower" : "snowblower"
            },
            "atmosphere" : {
                "fog" : "fog",
                "mist" : "mist",
                "dust" : "dust",
                "haze" : "haze",
                "hard to see" : "hard to see",
                "low visability" : "low visability"
            },
            "clear" : {
                "clear" : "clear",
                "nice day" : "nice day",
                "sunny" : "sunny",
                "sunshine" : "sunshine",
                "no clouds" : "no cloads",
                "calm" : "calm",
            },
            "clouds" : {
                "cloud" : "cloud",
                "cloudy" : "cloudy",
                "grey sky" : "grey sky",
                "overcast" : "overcast",
                "drab day" : "drab day",
                "no sun" : "no sun"
            },
            "extreme" : {
                "tornado" : "tornado",
                "tropical storm" : "tropical storm",
                "hurricane" : "hurricane",
                "hail" : "hail",
                "volcano" : "volcano",
                "cyclone" : "cyclone"

            },
            "additional" : {
                #this overlaps with alot of stuff
            }
        }
     

    def simplify_twitter_file (self):
        data_file_uri = 'data/twitter_data.txt'
        data_file = io.open(data_file_uri, 'r', newline='\r\n', encoding='utf8')

        organized_data_file_uri_json = 'data/twitter_data_formated.json'
        organized_data_file_json = io.open(organized_data_file_uri_json, 'w', encoding='utf8')
        for line in data_file:
            try:
                data = json.loads(line, encoding='utf8')
                if data['lang'] == "en":
                    json_str = json.dumps({'timestamp' : int(data['timestamp_ms'][:-3]),
                                            'date' : data['created_at'],
                                            'text' : data['text']}, ensure_ascii=False)
                    organized_data_file_json.write(unicode(json_str) + u'\r\n')
            except:
                print 'error'

    def generate_no_learning_estimate(self):
        sys.stdout = codecs.getwriter('utf8')(sys.stdout)
        sys.stderr = codecs.getwriter('utf8')(sys.stderr)

        data_file_uri = 'data/twitter_data_formated.json'
        data_file = io.open(data_file_uri, 'r', newline='\r\n', encoding='utf8')

        weather_file_uri = 'data/weatherData.json'
        weather_file = io.open(weather_file_uri, 'r', encoding='utf8')

        result_file_uri = 'data/resultNovice.csv'
        result_file = io.open(result_file_uri, 'w', encoding='utf8')
        result_file.write(u'Predicted, Actual \n')

        weather_line_current = json.loads(weather_file.readline(), encoding='utf8')
        weather_line_next = weather_line_current

        print 'before op'

        count = 0
        catagorie_scores = {
                "thunderstorms" : 0, "drizzle": 0, "rain" : 0, "snow" : 0, "atmosphere" : 0,
                 "clear" : 0,"clouds" : 0, "extreme" : 0,"additional" : 0
            }

        previous_weather = 'clear'

        start_time = time.time()
        correct, total = 0, 0

        for line in data_file:
            data = json.loads(line, encoding='utf8')
            output_to_file = True
            #print weather_line_next['dt']

            while data['timestamp'] - weather_line_next['dt'] > 0:
                if output_to_file == True:
                    maxVotes = 0
                    maxCatagorie = previous_weather
                    for catagorie, vote_count in catagorie_scores.iteritems():
                        if vote_count > maxVotes:
                            maxCatagorie = catagorie
                            maxVotes = vote_count
                    previous_weather = maxCatagorie
                    if maxCatagorie == weather_line_current['weather'][0]['main'].strip().lower():
                        correct += 1
                    result_file.write(maxCatagorie + u',' + weather_line_current['weather'][0]['main'] + u'\n') #need to make this convert to catagories
                    total += 1
                    output_to_file = False

                catagorie_scores = {
                    "thunderstorms" : 0, "drizzle": 0, "rain" : 0, "snow" : 0, "atmosphere" : 0,
                    "clear" : 0,"clouds" : 0, "extreme" : 0,"additional" : 0
                }
                weather_line_current = weather_line_next
                text_line = weather_file.readline()
                if (text_line != ''):
                    weather_line_next = json.loads(text_line, encoding='utf8')
                else:
                    print "Used Tweet Count " + str(count + 1)
                    print "Correct Weathers " + str(correct)
                    print "Total Weathers " + str(total)
                    print "Percent Correct " + str(float(correct) / float(total))
                    print "Time " + str(float(time.time()) - float(start_time))
                    return
            
            text_array = re.findall(r"[\w']+", data['text'])
            #print text_array
            for word in text_array:
                for weather_catagorie in self.catagories:
                    if word.lower() in self.catagories[weather_catagorie]:
                        catagorie_scores[weather_catagorie] += 1
            count += 1
        print "Used Tweet Count " + str(count + 1)
        print "Correct Weathers " + str(correct)
        print "Total Weathers " + str(total)
        print "Percent Correct " + str(float(correct) / float(total))
        return
                        
                        
       
#Use =IF(TRIM(A2)=TRIM("Unknown"), "Unknown", IF(TRIM(A2)=TRIM(B2),"True","False")) in excel to compare results

if __name__ == '__main__':
    nl = NoviceLearner()
    #nl.simplify_twitter_file()
    nl.generate_no_learning_estimate()