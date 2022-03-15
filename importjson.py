import json
import requests
from datetime import datetime
import config
import sqlite3
import os
from imdb import IMDb

IMDbAPI = IMDb()

def callAPI(startDate, numDays, zipcode, lat, lng, radius, units):
	startDate =  startDate #Start date (yyyy-mm-dd). Schedules available starting with current day.
	if(numDays):
		numDays = numDays
	if(zipcode):
		zipcode = zipcode
	lat = ''
	lng = ''
	if(radius):
		radius = radius
	units = ''
	imageSize = ''
	imageText = ''
	market = ''
	api = config.xapi


	response = requests.get(
        url="https://api.internationalshowtimes.com/v4/movies/",
        params={
            "countries": "US",
            "location": "47.63371178611272,-122.31584169070375",
            "distance": "50",
            # "cinema_id": "48091", #uptown
            # "cinema_id": "48117", #film center
            # "cinema_id": "48153", #egyptiion
            # "cinema_id": "73899",
            # "city_ids": "4966",
            # "movie_id": "12664",
            # "time_to": "2016-05-01T00:00:00-08:00"
            # "fields": "cinema_movie_title",
            "fields": "title,id,runtime",

            
        },
        headers={
            "X-API-Key": config.xapi,
        },
    )

	return response.json()['movies']

def dumpToDatabase(jsonData):
	connect, cursor = createDatabase()

	x = 0
	while x < len(jsonData):
		tmsId = jsonData[x]['tmsId']
		currenttitle = jsonData[x]['title']

		try:
			shortDescription = jsonData[x]['shortDescription']
		except:
			shortDescription = ''
		try:
			rating = jsonData[x]['ratings'][0]['code']
		except:
			rating = ''
		try:
			advisories = jsonData[x]['advisories'][0]
		except:
			advisories = ''
		try:
			runTime = jsonData[x]['runTime']
		except:
			runTime = ''
		try:
			genres = jsonData[x]['genres'][0]
		except:
			genres = ''
		try:
			directors = jsonData[x]['directors'][0]
		except:
			directors = ''
		try:
			topCast = jsonData[x]['topCast'][0]
		except:
			topCast = ''
		try:
			releaseYear = jsonData[x]['releaseYear']
		except:
			releaseYear = ''
		try:
			releaseDate = jsonData[x]['releaseDate']
		except:	
			releaseDate = ''	
		try:
			officialUrl = jsonData[x]['officialUrl']
		except:
			officialUrl = ''

		# cursor.execute("SELECT posterURL FROM moviePosterDB WHERE title=?", (currenttitle,))
		posterURL = ''#cursor.fetchall()
		# try:
		# 	posterURL = posterURL[0][0]
		# except:
		# 	posterURL = ''

		currenttheatre = ""
		theaterCount = 0
		while theaterCount < len(jsonData[x]['showtimes']):
			currenttheatre = jsonData[x]['showtimes'][theaterCount]['theatre']['name']

			
			theatreID = jsonData[x]['showtimes'][theaterCount]['theatre']['id']
			movieTime = jsonData[x]['showtimes'][theaterCount]['dateTime']

			try:
				generalSettings = jsonData[x]['showtimes'][theaterCount]['quals']
			except:
				generalSettings = ""
			try:
				bargin = jsonData[x]['showtimes'][theaterCount]['barg']
			except:
				bargin = ""
			try:
				ticketURL = jsonData[x]['showtimes'][theaterCount]['ticketURI']
			except:
				ticketURL = ""

			#(tmsId text, title text, theatreName text, theatreID text, movieTime date, generalSettings text, officialUrl text, posterURL text, bargin text, ticketURL text)''')
			cursor.execute("INSERT INTO movieTimeDB VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (tmsId, currenttitle, currenttheatre, theatreID, movieTime, generalSettings, officialUrl, posterURL, bargin, ticketURL))	

			theaterCount+=1

		cursor.execute("SELECT MIN(movieTime) AS First FROM movieTimeDB WHERE tmsId = ?", (tmsId,))
		showingsStart = cursor.fetchall()
		showingsStart = showingsStart[0][0]
		cursor.execute("SELECT MAX(movieTime) AS Last FROM movieTimeDB WHERE tmsId = ?", (tmsId,))
		showingsEnd = cursor.fetchall()
		showingsEnd = showingsEnd[0][0]
		cursor.execute("SELECT DISTINCT theatreName FROM movieTimeDB WHERE tmsId = ?", (tmsId,))
		whichTheaters = cursor.fetchall()

		i = len(whichTheaters)
		j = 1
		whichTheatersReturn = whichTheaters[0][0]
		while j < i:
			whichTheatersReturn = whichTheatersReturn + "; " + whichTheaters[j][0]
			j+=1

		#(tmsId text, title text, shortDescription text, rating text, advisories text, runTime text, officialUrl text, posterURL text, genres text, directors text, topCast text, releaseYear text, releaseDate date, 
	    #           showingsStart text, showingsEnd text, theatresShowing text)''')

		cursor.execute("INSERT INTO movieInfoDB VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (tmsId, currenttitle, shortDescription, rating, advisories, runTime, officialUrl, posterURL, genres, directors, topCast, releaseYear, releaseDate, showingsStart, showingsEnd, whichTheatersReturn))

		x+=1

	connect.commit()
	connect.close()

def returnMoviesShowing():
	connect = sqlite3.connect('movietimes.sqlite')
	cursor = connect.cursor()
	cursor.execute("SELECT posterURL, officialUrl, title, rating, runTime, directors, releaseYear, shortDescription, showingsStart, showingsEnd, theatresShowing, tmsId FROM movieInfoDB")
	moviesPlayingNearYou = cursor.fetchall()
	tosendback = sorted(moviesPlayingNearYou, key=lambda x: x[2].lower()) #Sort by title which is the 3rd element in query
	connect.close()
	return tosendback

def returnOneMoviesInfo(movieid):
	connect = sqlite3.connect('movietimes.sqlite')
	cursor = connect.cursor()
	cursor.execute("SELECT posterURL, officialUrl, title, rating, runTime, directors, releaseDate, shortDescription, showingsStart, showingsEnd, theatresShowing, tmsId FROM movieInfoDB WHERE tmsId = ?", (movieid,))
	moviesPlayingNearYou = cursor.fetchall()
	tosendback = sorted(moviesPlayingNearYou, key=lambda x: x[2].lower()) #Sort by title which is the 3rd element in query
	connect.close()
	return tosendback

def returnOneMoviesTimes(movieid):
	connect = sqlite3.connect('movietimes.sqlite')
	cursor = connect.cursor()
	cursor.execute("SELECT theatreName, theatreID, movieTime, generalSettings, bargin, ticketURL FROM movieTimeDB WHERE tmsId = ?", (movieid,))
	showtimes = cursor.fetchall()
	connect.close()
	return showtimes

def searchDatabase(findmovie, theatreName, movieInfo, alist, dolby, imax):
	connect = sqlite3.connect('movietimes.sqlite')
	cursor = connect.cursor()

	if(alist):
		alist = 'AMC'
	else:
		alist = ''
	if(dolby):
		dolby = 'Dolby'
	else:
		dolby = ''
	if(imax):
		imax = 'IMAX'
	else:
		imax = ''

	# (tmsId text, title text, theatreName text, theatreID text, movieTime date, generalSettings text, officialUrl text, posterURL text, bargin text, ticketURL text)''')

	query = """SELECT title, theatreName, movieTime, generalSettings, bargin, ticketURL, tmsId
				FROM movieTimeDB 
				WHERE title LIKE '%'||?||'%' 
				AND theatreName LIKE '%'||?||'%' 
				AND generalSettings LIKE '%'||?||'%' 
				AND theatreName LIKE '%'||?||'%' 
				AND generalSettings LIKE '%'||?||'%' 
				AND (title LIKE '%'||?||'%' OR generalSettings LIKE '%'||?||'%') 
				"""


	searchParameters = (findmovie,theatreName,movieInfo,alist,dolby,imax,imax)
	# connect.set_trace_callback(print)

	cursor.execute(query,searchParameters)

	data = cursor.fetchall()

	return data

def closeDatabase():
	try:
		# Save (commit) the changes
		connect.commit()
		connect.close()
	except:
		pass

