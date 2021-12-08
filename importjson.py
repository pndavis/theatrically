import json
import requests
from datetime import datetime
import config
import pandas as pd
import sqlite3
from imdb import IMDb

ia = IMDb()

# get a movie and print its director(s)

found = ia.search_movie('cmon cmon')
print(found[0].movieID)
movies = ia.get_movie(found[0].movieID)
# print(movies.infoset2keys)
# the_matrix = ia.get_movie('0133093')
# for director in the_matrix['directors']:
#     print(director['name'])

# show all information that are currently available for a movie
# print(sorted(the_matrix.keys()))

# show all information sets that can be fetched for a movie
# print(ia.get_movie_infoset())

# update a Movie object with more information
# ia.update(the_matrix, ['technical'])
# show which keys were added by the information set
# print(the_matrix.infoset2keys['technical'])
# print one of the new keys
print(movies.get('full-size cover url'))


con = sqlite3.connect('movietimes.sqlite')
cur = con.cursor()

cur.execute('DROP TABLE movieTimeDB')
# Create table
cur.execute('''CREATE TABLE movieTimeDB
               (title text, theatreName text, theatreID text, movieTime text, generalSettings text)''')

# Insert a row of data
# cur.execute("INSERT INTO movieTimeDB VALUES ('CMON','SIFF','123','100','dolby')")



startDate = '&startDate=2021-12-07' #Start date (yyyy-mm-dd). Schedules available starting with current day.
numDays = ''
zipcode = '&zip=98102'
lat = ''
lng = ''
radius = '&radius=30'
units = '&units=mi'
imageSize = ''
imageText = ''
market = ''
api = config.api_key

# gracenote = 'http://data.tmsapi.com/v1.1/movies/showings?' + startDate + zipcode + radius + api
# response = requests.get(gracenote)
# jsonData = response.json()

f = open('cmon.json')
jsonData = json.load(f)


# print(jsonData[0])
# print(type(showtimeone))
# print(type(jsonData))
# print(jsonData[0]['showtimes'][0]['theatre']['name'])

# itish = len(jsonData[0]['showtimes'])
# print(itish)


# print()
# print()

x = 0
while x < len(jsonData):
	# print("Showtimes for " + jsonData[x]['title'] + " on " + datetime.strptime(jsonData[x]['showtimes'][0]['dateTime'], "%Y-%m-%dT%H:%M").strftime('%B %d'))
	count = 0
	currenttheatre = ""
	lasttheatre = ""
	while count < len(jsonData[x]['showtimes']):
		currenttheatre = jsonData[x]['showtimes'][count]['theatre']['name']
		premium = ""

		currenttitle = jsonData[x]['title']
		theatreID = jsonData[x]['showtimes'][count]['theatre']['id']
		currentTime = jsonData[x]['showtimes'][count]['dateTime']

		try:
			details = jsonData[x]['showtimes'][count]['quals']
			# if "Dolby Cinema" in details:
			# 	premium = "Dolby Cinema"
			# if "IMAX" in details:
			# 	premium = "IMAX"
		except:
			details = ""


		# (title text, theatreName text, theatreID text, movieTime text, generalSettings text)

		cur.execute("INSERT INTO movieTimeDB VALUES (?, ?, ?, ?, ?)", (currenttitle, currenttheatre, theatreID, currentTime, details))	

		# if currenttheatre == lasttheatre:
		# 	print (datetime.strptime(jsonData[x]['showtimes'][count]['dateTime'], "%Y-%m-%dT%H:%M").strftime('%I:%M%p').lower() + " " + premium)
		# else:
		# 	print()
		# 	print (currenttheatre)
		# 	print (datetime.strptime(jsonData[x]['showtimes'][count]['dateTime'], "%Y-%m-%dT%H:%M").strftime('%I:%M%p').lower() + " " + premium)

		# lasttheatre = currenttheatre

		count+=1
	x+=1

# cur.execute('SELECT title, movieTime FROM movieTimeDB WHERE theatreName = "AMC Loews Alderwood Mall 16"')
# print(cur.fetchall())

con.commit()
df = pd.read_sql_query("SELECT theatreName, title, movieTime FROM movieTimeDB WHERE title = 'Benedetta'", con)

# print(df)

df = pd.read_sql_query("SELECT theatreName, title, movieTime FROM movieTimeDB WHERE theatreName = 'AMC Dine-In Seattle 10'", con)

# print(df)



# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()

