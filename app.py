from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from jinja2 import environment 
from importjson import *


app = Flask(__name__)
Bootstrap(app)

@app.template_filter()
def format_Month(value):
    # 2022-02-21T16:00
    return datetime.strptime(value, '%Y-%m-%dT%H:%M').strftime('%b %d')

@app.template_filter()
def format_Showtime(value):
    # 2022-02-21T16:00
    return datetime.strptime(value, '%Y-%m-%dT%H:%M').strftime('%m/%d at %-I:%M%p')

    PT01H52M
@app.template_filter()
def format_Runtime(value):
    # PT01H37M
    try:
        return datetime.strptime(value, 'PT%HH%MM').strftime('%Hh %Mm')
    except:
        return value

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/moviesShowing', methods=['POST'])
def moviesShowing():
    startDate = request.form['startDate']
    numDays = request.form['numDays']
    zipcode = request.form['zipcode']
    # lat = request.form['lat']
    # lng = request.form['lng']
    radius = request.form['radius']
    # units = request.form['units']
    lat = ''
    lng = ''
    units = ''

    jsonData = getGracenoteAPI(startDate, numDays, zipcode, lat, lng, radius, units)
    # jsonData = pullFromJson()

    if(jsonData == None):
        movieList = "Ran out of api calls"
        return render_template("404.html")
    else:
        # createPosterDatabase(jsonData)
        # updatePosterDatabase(jsonData)
        dumpToDatabase(jsonData)
        movieList = returnMoviesShowing()
        return render_template("moviesShowing.html",moviesShowing=movieList)

@app.route('/movielist')
def movieList():
    movieList = returnMoviesShowing()
    return render_template("moviesShowing.html",moviesShowing=movieList)

@app.route('/showtimes', methods=['POST'])
def returnMovieTimes():      

    movieName = request.form['movie']
    theatreName = request.form['theater']
    movieInfo = request.form['features']
    amc = request.form.get('amc')
    dolby = request.form.get('Dolby')
    imax = request.form.get('Imax')

    times = searchDatabase(movieName, theatreName, movieInfo, amc, dolby, imax)

    return render_template("showtimes.html",showtimes=times)

@app.route('/movie/<movieid>')
def profile(movieid):
    oneInfo = returnOneMoviesInfo(movieid)
    oneShowtimes = returnOneMoviesTimes(movieid)
    # print(oneInfo)
    # print(oneShowtimes)
    return render_template("moviepage.html", movieInfo=oneInfo, movieTime=oneShowtimes)

@app.route('/about')
def about():
	return render_template("about.html")

if __name__ == "__main__":
    app.run()