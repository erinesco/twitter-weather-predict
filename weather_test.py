# import openweather 
# from datetime import datetime

# #create client 
# ow = openweather.OpenWeather() 

# print "looking for local station"
# #find weather stations near me 
# #stations = ow.find_stations_near( 
# #	71.0589, #longitute 
# #	42.3601, #lattitute 
# #	50       #kilometer radius  
# #	)
# print "found local station"

# #iterate results 
# # for station in stations: 
# # 	print station 

# print "getting stuff from random station"
# #get current weather at station with id 4885 
# print ow.get_weather(4885)

# #historic weather 
# start_date = datetime(2016, 9, 01)
# end_date = datetime(2016, 10, 01)
import time
import json 
import requests
while(True): 
	if(0 == time.time() % 1800):  
		r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Boston&APPID=b547b476918e843f46da5af988e7c31a')
		print (r.json())
		print time.time()
		with open('weatherData.json', 'a') as json_file: 
			json_file.write("{}\n".format(json.dumps(r.json())))
		