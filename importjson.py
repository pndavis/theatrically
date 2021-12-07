import json
import requests
from datetime import datetime
import config

startDate = '&startDate=2021-12-07' #Start date (yyyy-mm-dd). Schedules available starting with current day.
numDays = ''
zipcode = '&zip=98102'
lat = ''
lng = ''
radius = '&radius=3'
units = '&units=mi'
imageSize = ''
imageText = ''
market = ''
api = config.api_key

gracenote = 'http://data.tmsapi.com/v1.1/movies/showings?' + startDate + zipcode + radius + api
response = requests.get(gracenote)
jsonData = response.json()

# f = open('cmon.json')
# jsonData = json.load(f)


# print(jsonData[0])
# print(type(showtimeone))
# print(type(jsonData))
# print(jsonData[0]['showtimes'][0]['theatre']['name'])

# itish = len(jsonData[0]['showtimes'])
# print(itish)


print()
print()

x = 0
while x < len(jsonData):
	print("Showtimes for " + jsonData[x]['title'] + " on " + datetime.strptime(jsonData[x]['showtimes'][0]['dateTime'], "%Y-%m-%dT%H:%M").strftime('%B %d'))
	count = 0
	currenttheatre = ""
	lasttheatre = ""
	while count < len(jsonData[x]['showtimes']):
		currenttheatre = jsonData[x]['showtimes'][count]['theatre']['name']
		premium = ""

		try:
			details = jsonData[x]['showtimes'][count]['quals']
			if "Dolby Cinema" in details:
				premium = "Dolby Cinema"
			if "IMAX" in details:
				premium = "IMAX"
		except:
			pass

		if currenttheatre == lasttheatre:
			print (datetime.strptime(jsonData[x]['showtimes'][count]['dateTime'], "%Y-%m-%dT%H:%M").strftime('%I:%M%p').lower() + " " + premium)
		else:
			print()
			print (currenttheatre)
			print (datetime.strptime(jsonData[x]['showtimes'][count]['dateTime'], "%Y-%m-%dT%H:%M").strftime('%I:%M%p').lower() + " " + premium)

		lasttheatre = currenttheatre
		count+=1
	x+=1
	print()

print()

