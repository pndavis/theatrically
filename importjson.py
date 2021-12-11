import json
import requests
from datetime import datetime
import config
import pandas as pd
import sqlite3
from imdb import IMDb

IMDbAPI = IMDb()


def createDatabase():
	con = sqlite3.connect('movietimes.sqlite')
	cur = con.cursor()

	try:
		cur.execute('DROP TABLE movieTimeDB')
	except:
		pass
	# Create table
	cur.execute('''CREATE TABLE movieTimeDB
	               (title text, theatreName text, theatreID text, movieTime date, generalSettings text, posterURL text)''')

	return con, cur

def createPosterDatabase():
	con = sqlite3.connect('movietimes.sqlite')
	cursor = con.cursor()

	try:
		cursor.execute('DROP TABLE moviePosterDB')
	except:
		pass

	try:
		cursor.execute('''CREATE TABLE moviePosterDB
	               (title text, posterURL text)''')
	except:
		pass

	jsonData = pullFromJson()
	x = 0
	while x < len(jsonData):

		fullMovieName = jsonData[x]['title']
		movieName = (jsonData[x]['title']).replace(': The IMAX 2D Experience', '')
		movieName.replace(' -- The IMAX 2D Experience', '')

		print(fullMovieName + " looking for: " + movieName)
		lookUpMovie = IMDbAPI.search_movie(movieName)
		
		try:
			print("Found movie " + lookUpMovie[0].movieID)
			currentMovie = IMDbAPI.get_movie(lookUpMovie[0].movieID)
			posterURL = currentMovie.get('full-size cover url')
		except:
			posterURL = "Movie_not_found"
			print("Movie not found")
		print(posterURL)
		# posterURL = "https://m.media-amazon.com/images/M/MV5BMzkwZWJhOTUtZTJkMC00OWQ5LTljZDctYzgxNWFiYjEyZjZiXkEyXkFqcGdeQXVyMDA4NzMyOA@@.jpg"

		cursor.execute("INSERT INTO moviePosterDB VALUES (?, ?)", (fullMovieName, posterURL))
		x+=1

	con.commit()
	con.close()

	print("Database created")

# def updatePosterDatabase():
	# con = sqlite3.connect('movietimes.sqlite')
	# cursor = con.cursor()

	# jsonData = pullFromJson()
	# x = 0
	# while x < len(jsonData):

	# 	fullMovieName = jsonData[x]['title']
	# 	movieName = (jsonData[x]['title']).replace(': The IMAX 2D Experience', '')
	# 	movieName.replace(' -- The IMAX 2D Experience', '')

	# 	print(fullMovieName + " looking for: " + movieName)
	# 	lookUpMovie = IMDbAPI.search_movie(movieName)
		
	# 	try:
	# 		print("Found movie " + lookUpMovie[0].movieID)
	# 		currentMovie = IMDbAPI.get_movie(lookUpMovie[0].movieID)
	# 		posterURL = currentMovie.get('full-size cover url')
	# 	except:
	# 		posterURL = "Movie_not_found"
	# 		print("Movie not found")
	# 	print(posterURL)

	# 	cursor.execute("INSERT INTO moviePosterDB VALUES (?, ?)", (fullMovieName, posterURL))
	# 	x+=1
	# con.commit()
	# con.close()
	# print("Poster Database updated")


def pullFromJson():
	f = open('90days.json')
	jsonData = json.load(f)

	return jsonData

def getGracenoteAPI(startDate, numDays, zipcode, lat, lng, radius, units):
	startDate =  '&startDate=' + startDate #Start date (yyyy-mm-dd). Schedules available starting with current day.
	if(numDays):
		numDays = '&numDays=' + numDays
	if(zipcode):
		zipcode = '&zip=' + zipcode
	lat = ''
	lng = ''
	if(radius):
		radius = '&radius=' + radius
	units = ''
	imageSize = ''
	imageText = ''
	market = ''
	api = config.api_key

	gracenote = 'http://data.tmsapi.com/v1.1/movies/showings?' + startDate + numDays + zipcode + radius + api
	print(gracenote)
	response = requests.get(gracenote)

	try:
		jsonData = response.json()
		return jsonData
	except:
		return None
	

	


def dumpToDatabase(jsonData):
	con, cursor = createDatabase()

	x = 0
	moviesPlayingNearYou = []
	# allMovies = []
	while x < len(jsonData):
		# allMovies.append(jsonData[x]['title'])
		count = 0
		currenttheatre = ""
		currenttitle = jsonData[x]['title']

		cursor.execute("SELECT posterURL FROM moviePosterDB WHERE title=?", (currenttitle,))
		posterURL = cursor.fetchall()
		try:
			posterURL = posterURL[0][0]
		except:
			posterURL = ''

		while count < len(jsonData[x]['showtimes']):
			currenttheatre = jsonData[x]['showtimes'][count]['theatre']['name']

			
			theatreID = jsonData[x]['showtimes'][count]['theatre']['id']
			currentTime = jsonData[x]['showtimes'][count]['dateTime']

			try:
				details = jsonData[x]['showtimes'][count]['quals']
			except:
				details = ""


			cursor.execute("INSERT INTO movieTimeDB VALUES (?, ?, ?, ?, ?, ?)", (currenttitle, currenttheatre, theatreID, currentTime, details, posterURL))	

			count+=1
		cursor.execute("SELECT title, MIN(movieTime) AS First, MAX(movieTime) AS Last, posterURL FROM movieTimeDB WHERE title = ?", (currenttitle,))
		moviesPlayingNearYou.append(cursor.fetchall())
		x+=1
	con.commit()
	con.close()
	

	# moviesPlayingNearYou = moviesPlayingNearYou[0]
	# print(moviesPlayingNearYou)
	tosendback = sorted(moviesPlayingNearYou, key=lambda x: x[0][0].lower())
	# print(tosendback)
	return tosendback


def searchDatabase(findmovie, theatreName, movieInfo, alist, dolby, imax):
	con = sqlite3.connect('movietimes.sqlite')
	cursor = con.cursor()

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

	query = """SELECT title, theatreName, STRFTIME('%m/%d at %H:%M', movieTime), generalSettings 
				FROM movieTimeDB 
				WHERE title LIKE '%'||?||'%' 
				AND theatreName LIKE '%'||?||'%' 
				AND generalSettings LIKE '%'||?||'%' 
				AND theatreName LIKE '%'||?||'%' 
				AND generalSettings LIKE '%'||?||'%' 
				AND (title LIKE '%'||?||'%' OR generalSettings LIKE '%'||?||'%') 
				"""


	searchParameters = (findmovie,theatreName,movieInfo,alist,dolby,imax,imax)
	# print(type(searchParameters))
	# print(searchParameters)
	# print(query, searchParameters)
	# query = "SELECT title, theatreName, STRFTIME('%m/%d at %H:%M', movieTime), generalSettings FROM movieTimeDB WHERE theatreName LIKE '%" + alist + "%' AND generalSettings LIKE '%" + dolby + "%' AND (title LIKE '%" + imax + "%' OR generalSettings LIKE '%" + imax + "%') AND title LIKE '%" + findmovie + "%''"
	# print(query)
	con.set_trace_callback(print)

	cursor.execute(query,searchParameters)

	# cursor.execute("SELECT title, theatreName, STRFTIME('%m/%d at %H:%M', movieTime), generalSettings FROM movieTimeDB WHERE generalSettings LIKE %(?)% AND title = (?)", (premium, findmovie))
	# cursor.execute("SELECT title, theatreName, movieTime, generalSettings FROM movieTimeDB WHERE title = '%s'" % (findmovie))
	data = cursor.fetchall()
	# print(data)
	# df = pd.read_sql_query("SELECT title, theatreName, movieTime, generalSettings FROM movieTimeDB WHERE title = '%s'" % (findmovie), con)
	# print(pd.read_sql_query("SELECT title, theatreName, movieTime, generalSettings FROM movieTimeDB WHERE title = 'Dune'", con))
	# df = pd.read_sql_query("SELECT title, theatreName, movieTime FROM movieTimeDB WHERE generalSettings LIKE '%70mm%'", con)

	# print(data)

	# df = pd.read_sql_query("SELECT theatreName, title, movieTime FROM movieTimeDB WHERE theatreName = 'AMC Dine-In Seattle 10'", con)

	# print(df)
	return data

def closeDatabase():
	try:
		# Save (commit) the changes
		con.commit()
		# We can also close the connection if we are done with it.
		# Just be sure any changes have been committed or they will be lost.
		con.close()
	except:
		pass

