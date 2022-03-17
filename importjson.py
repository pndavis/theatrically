import json
import requests
from datetime import datetime
import config
import sqlite3
import os
from imdb import IMDb

IMDbAPI = IMDb()
connect = sqlite3.connect(':memory:', check_same_thread=False)
cursor = connect.cursor()

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
            "fields": "title,id,runtime,imdb_id",

            
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

def createDatabase():
	try:
		cursor.execute('DROP TABLE showtimes')
	except:
		pass
	try:
		cursor.execute('DROP TABLE movies')
	except:
		pass
	try:
		cursor.execute('DROP TABLE cinemas')
	except:
		pass

	cursor.execute('''CREATE TABLE showtimes
				(show_id text, cinema_id text, movie_id text, start_at text, language text, subtitle_language text, auditorium text, threeD text, imax text, booking_type text, booking_link text, cinema_movie_title text)''')
	
	cursor.execute('''CREATE TABLE movies
	               (movie_id text, title text, poster_thumbnail text, imdb_id text)''')
				   
	cursor.execute('''CREATE TABLE cinemas
					(cinema_id text, cinema_name text)''')



def getAPI(startDate, numDays, zipcode, lat, lng, distance):

	distance = 10
	lat = '47.608013'
	lon = '-122.335167'
	location = lat + "," + lon
	
	try:
		api = os.environ["xapi"]
	except:
		api = config.xapi

	response = requests.get(
		url="https://api.internationalshowtimes.com/v4/showtimes/",
		params={
			"countries": "US",
			"location": location,
			"distance": distance,
			# "time_to": "2022-03-",
			"fields": "id,cinema_id,movie_id,start_at,language,subtitle_language,auditorium,is_3d,is_imax,booking_type,booking_link,cinema_movie_title",
			"append": "movies,cinemas",
			"movie_fields": "id,title,poster_image_thumbnail,imdb_id",
			"cinema_fields": "id,name",
			
			
			
			
		},
		headers={
			"X-API-Key": api,
		},
	)
	
	return response

def dumpToDatabase(jsonData):
	createDatabase()

	
	showtimeCount = 0
	while showtimeCount < len(jsonData['showtimes']):
		show_id = jsonData['showtimes'][showtimeCount]['id']
		cinema_id = jsonData['showtimes'][showtimeCount]['cinema_id']
		movie_id = jsonData['showtimes'][showtimeCount]['movie_id']
		start_at = jsonData['showtimes'][showtimeCount]['start_at']
		print(start_at)
		language = jsonData['showtimes'][showtimeCount]['language']
		subtitle_language = jsonData['showtimes'][showtimeCount]['subtitle_language']
		auditorium = jsonData['showtimes'][showtimeCount]['auditorium']
		is_3d = jsonData['showtimes'][showtimeCount]['is_3d']
		is_imax = jsonData['showtimes'][showtimeCount]['is_imax']
		booking_type = jsonData['showtimes'][showtimeCount]['booking_type']
		booking_link = jsonData['showtimes'][showtimeCount]['booking_link']
		cinema_movie_title = jsonData['showtimes'][showtimeCount]['cinema_movie_title']
		
		# print(cinema_id + " is " + jasonData['cinemas'][])
		
		cursor.execute("INSERT INTO showtimes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (show_id, cinema_id, movie_id, start_at, language, subtitle_language, auditorium, is_3d, is_imax, booking_type, booking_link, cinema_movie_title))
		
		# cursor.execute("SELECT * from showtimes")
		# print(cursor.fetchall())
		
		showtimeCount+=1
	
	movieCount = 0
	while movieCount < len(jsonData['movies']):
		
		movie_id = jsonData['movies'][movieCount]['id']
		title = jsonData['movies'][movieCount]['title']
		poster = jsonData['movies'][movieCount]['poster_image_thumbnail']
		imdb_id = jsonData['movies'][movieCount]['imdb_id']
		
		cursor.execute("INSERT INTO movies VALUES (?, ?, ?, ?)", (movie_id, title, poster, imdb_id))
		#{'id': '14262', 'title': 'I Am Here', 'poster_image_thumbnail': 'https://image.tmdb.org/t/p/w154/yA06Duc3TgvDvIJn72sOB0G19mH.jpg'
		movieCount+=1
		
	cinemaCount = 0
	while cinemaCount < len(jsonData['cinemas']):
		cinema_id = jsonData['cinemas'][cinemaCount]['id']
		cinema_name = jsonData['cinemas'][cinemaCount]['name']
		
		cursor.execute("INSERT INTO cinemas VALUES (?, ?)", (cinema_id, cinema_name))
		cinemaCount+=1
		

def returnMoviesShowing():
	cursor.execute("SELECT show_id, cinema_id, showtimes.movie_id, start_at, language, subtitle_language, booking_link, cinema_movie_title, title, poster_thumbnail, imdb_id FROM showtimes INNER JOIN movies on showtimes.movie_id = movies.movie_id")
	moviesPlayingNearYou = cursor.fetchall()
	return moviesPlayingNearYou

def returnOneMoviesInfo(movieid):
	
	cursor.execute("SELECT posterURL, officialUrl, title, rating, runTime, directors, releaseDate, shortDescription, showingsStart, showingsEnd, theatresShowing, tmsId FROM movieInfoDB WHERE tmsId = ?", (movieid,))
	moviesPlayingNearYou = cursor.fetchall()
	tosendback = sorted(moviesPlayingNearYou, key=lambda x: x[2].lower()) #Sort by title which is the 3rd element in query
	return tosendback

def returnOneMoviesTimes(movieid):
	
	cursor.execute("SELECT theatreName, theatreID, movieTime, generalSettings, bargin, ticketURL FROM movieTimeDB WHERE tmsId = ?", (movieid,))
	showtimes = cursor.fetchall()
	return showtimes

def searchDatabase(findmovie, theatreName, movieInfo, alist, dolby, imax):
	

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

