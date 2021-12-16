from flask import Flask, request, render_template
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


# <!-- <td>{{macros.datetime.strptime(row[0][1], "%Y-%m-%dT%H:%M").strftime("%b %d at %I:%M%p")}}</td> -->


from importjson import *


app = Flask(__name__)


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

    jsonData = getGracenoteAPI(startDate, numDays, zipcode, lat, lng, radius, units)
    # jsonData = pullFromJson()

    if(jsonData == None):
        moviesShowing="Ran out of api calls"
        return render_template("moviesShowing.html")
    else:
        # createPosterDatabase(jsonData)
        updatePosterDatabase(jsonData)
        moviesShowing = (dumpToDatabase(jsonData))
        return render_template("moviesShowing.html",moviesShowing=moviesShowing)

@app.route('/showtimes', methods=['POST'])
def returnMovieTimes():

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