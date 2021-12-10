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
# print(found[0].movieID)
# movies = ia.get_movie(found[0].movieID)
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
# print(movies.get('full-size cover url'))

def createDatabase():
	con = sqlite3.connect('movietimes.sqlite')
	cur = con.cursor()

	try:
		cur.execute('DROP TABLE movieTimeDB')
	except:
		pass
	# Create table
	cur.execute('''CREATE TABLE movieTimeDB
	               (title text, theatreName text, theatreID text, movieTime date, generalSettings text)''')

	return con, cur




def pullFromJson():
	f = open('90days.json')
	jsonData = json.load(f)

	return jsonData

def getGracenoteAPI(startDate1, numDays1, zipcode1, radius1):
	startDate = '&startDate=2021-12-09' #Start date (yyyy-mm-dd). Schedules available starting with current day.
	numDays = '&numDays=90'
	zipcode = '&zip=98102'
	lat = ''
	lng = ''
	radius = '&radius=5'
	units = ''
	imageSize = ''
	imageText = ''
	market = ''
	api = config.api_key

	gracenote = 'http://data.tmsapi.com/v1.1/movies/showings?' + startDate1 + numDays1 + zipcode1 + radius1 + api
	response = requests.get(gracenote)

	try:
		jsonData = response.json()
		return jsonData
	except:
		return None
	

	


def dumpToDatabase(jsonData):
	con, cursor = createDatabase()
	x = 0
	allMovies = []
	while x < len(jsonData):
		allMovies.append(jsonData[x]['title'])
		count = 0
		currenttheatre = ""
		lasttheatre = ""
		posterURL =''
		while count < len(jsonData[x]['showtimes']):
			currenttheatre = jsonData[x]['showtimes'][count]['theatre']['name']
			premium = ""

			currenttitle = jsonData[x]['title']
			theatreID = jsonData[x]['showtimes'][count]['theatre']['id']
			currentTime = jsonData[x]['showtimes'][count]['dateTime']

			try:
				details = jsonData[x]['showtimes'][count]['quals']
				if "Dolby Cinema" in details:
					premium = "Dolby Cinema"
				if "IMAX" in details:
					premium = "IMAX"
			except:
				details = ""


			# (title text, theatreName text, theatreID text, movieTime text, generalSettings text)

			cursor.execute("INSERT INTO movieTimeDB VALUES (?, ?, ?, ?, ?)", (currenttitle, currenttheatre, theatreID, currentTime, details))	

			# if currenttheatre == lasttheatre:
			# 	print (datetime.strptime(jsonData[x]['showtimes'][count]['dateTime'], "%Y-%m-%dT%H:%M").strftime('%I:%M%p').lower() + " " + premium)
			# else:
			# 	print()
			# 	print (currenttheatre)
			# 	print (datetime.strptime(jsonData[x]['showtimes'][count]['dateTime'], "%Y-%m-%dT%H:%M").strftime('%I:%M%p').lower() + " " + premium)

			# lasttheatre = currenttheatre

			count+=1
		x+=1
	con.commit()

	query = "SELECT DISTINCT title FROM movieTimeDB"
	cursor.execute(query)
	allMovieTitles = cursor.fetchall()
	print(allMovieTitles)


	con.close()
	# print (allMovies)
	# print(type(allMovies)) 
	return allMovieTitles

def searchDatabase(findmovie, alist, dolby, imax):
	# print("What movie do you want to see showtimes for?")
	# input1 = str(input())
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
				AND (title LIKE '%'||?||'%' OR generalSettings LIKE '%'||?||'%') 
				"""


	searchParameters = (findmovie,alist,dolby,imax,imax)
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
	print(data)
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

