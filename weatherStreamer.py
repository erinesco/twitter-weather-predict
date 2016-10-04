
import time, json, requests
while(True): 
	# Record weather every half hour
	if(0 == time.time() % 1800):  
		# json weather request for openweather 
		# uses api key that can request weather 60x/hour
		r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Boston&APPID=b547b476918e843f46da5af988e7c31a')
		print (r.json())
		print time.time()
		# append data to json file. 
		# if program is stopped it will not overwrite file
		with open('weatherData.json', 'a') as json_file: 
			json_file.write("{}\n".format(json.dumps(r.json())))
		