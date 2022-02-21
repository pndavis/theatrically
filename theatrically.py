from flask import Flask, request, render_template
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap


# <!-- <td>{{macros.datetime.strptime(row[0][1], "%Y-%m-%dT%H:%M").strftime("%b %d at %I:%M%p")}}</td> -->


from importjson import *

# global movieList


app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/moviesShowing', methods=['POST'])
def moviesShowing():
    

    startDate = request.form['startDate']
    numDays = request.form['numDays']
    zipcode = request.form['zipcode']
    lat = request.form['lat']
    lng = request.form['lng']
    radius = request.form['radius']
    units = request.form['units']

    #jsonData = getGracenoteAPI(startDate, numDays, zipcode, lat, lng, radius, units)
    jsonData = pullFromJson()

    if(jsonData == None):
        movieList = "Ran out of api calls"
        return render_template("404.html")
    else:
        # createPosterDatabase(jsonData)
        # updatePosterDatabase(jsonData)
        movieList = (dumpToDatabase(jsonData))
        return render_template("moviesShowing.html",moviesShowing=movieList)

    

# @app.route('/moviesShowing')
# def moviesShowingReturn():
#     return render_template("moviesShowing.html",moviesShowing=movieList)

@app.route('/showtimes', methods=['POST'])
def returnMovieTimes():

    if request.form['action'] == 'home':
        return render_template("homepage.html")
    elif request.form['action'] == 'showings':
        return render_template("moviesShowing.html")
    elif request.form['action'] == 'findmovies':
        

        movieName = request.form['movie']
        theatreName = request.form['theater']
        movieInfo = request.form['features']
        alist = request.form.get('alist')
        dolby = request.form.get('Dolby')
        imax = request.form.get('Imax')

        times = searchDatabase(movieName, theatreName, movieInfo, alist, dolby, imax)

        return render_template("showtimes.html",showtimes=times)

# @app.route('/movie/<string:id>',methods=['GET'])
# def moviepage(id):
#     return id
    

if __name__ == "__main__":
    app.run()