import json
from datetime import datetime
from datetime import timedelta




f = open('90days.json')
jsonData = json.load(f)

class Showtimes:
	def __init__(self, jsonShowings):
		self.theatreID = jsonShowings['theatre']['id']
		self.theatreName = jsonShowings['theatre']['name']
		self.dateTime = datetime.strptime(jsonShowings['dateTime'], '%Y-%m-%dT%H:%M')
		try:
			self.quals = jsonShowings['quals']
		except:
			self.quals = ""
		try:
			self.barg = jsonShowings['barg']
		except:
			self.barg = False
		try:
			self.ticketURI = jsonShowings['ticketURI']
		except:
			self.ticketURI = ""


	def sendshowtimes(self):
		return self.times

class Movie:
	def __init__(self, jsonMovie):
		self.tmsId = jsonMovie['tmsId']
		self.rootId = jsonMovie['rootId']
		self.subType = jsonMovie['subType']
		self.title = jsonMovie['title']
		try:
			self.titleLang = jsonMovie['titleLang']
		except:
			self.titleLang = ""
		try:
			self.shortDescription = jsonMovie['shortDescription']
		except:
			self.shortDescription = ""
		try:
			self.longDescription = jsonMovie['longDescription']
		except:
			self.longDescription = ""
		try:
			self.descriptionLang = jsonMovie['descriptionLang']
		except:
			self.descriptionLang = ""
		try:
			self.ratings = jsonMovie['ratings'][0]['code']
		except:
			self.ratings = ""
		try:
			self.genres = jsonMovie['genres']
		except:
			self.genres = ""
		try:
			self.topCast = jsonMovie['topCast']
		except:
			self.topCast = ""
		try:
			self.directors = jsonMovie['directors']
		except:
			self.directors = ""
		try:
			self.releaseYear = jsonMovie['releaseYear']
		except:
			self.releaseYear = ""
		try:
			self.releaseDate = datetime.strptime(jsonMovie['releaseDate'], '%Y-%m-%d')
		except:
			self.releaseDate = ""
		try:
			self.officialUrl = jsonMovie['officialUrl']
		except:
			self.officialUrl = ""
		try:
			self.runTime = jsonMovie['runTime'][2:]
		except:
			self.runTime = ""
		try:
			self.qualityRating = jsonMovie['qualityRating']['value']
		except:
			self.qualityRating = ""
		self.showtimes = []
		Showtimes(jsonMovie['showtimes'][0])


x = 0
while x < len(jsonData):
	movieOne = Movie(jsonData[x])
	print("title: " + movieOne.title)
	print("id: " + movieOne.tmsId)
	print("rootid: " + movieOne.rootId)
	print("Subtype: " + movieOne.subType)
	print("titlelang: " + movieOne.titleLang)
	print("short dec: " + movieOne.shortDescription)
	print("long desc: " + movieOne.longDescription)
	print("desc lang: " + movieOne.descriptionLang)
	print("rtings: " + movieOne.ratings)
	print("genres: ", movieOne.genres)
	print("topcast: ", movieOne.topCast)
	print("directors: ", movieOne.directors)
	print("Rlease year: " + str(movieOne.releaseYear))
	print(movieOne.releaseDate)
	print("url: " + movieOne.officialUrl)
	print("runtime: " + movieOne.runTime)
	print("quality: " + movieOne.qualityRating)
	print(movieOne.showtimes.dateTime.strftime('Showtime at %B %d, at %I:%M%p'))
	print()
	x+=1




