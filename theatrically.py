from flask import Flask, request, render_template
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


# <!-- <td>{{macros.datetime.strptime(row[0][1], "%Y-%m-%dT%H:%M").strftime("%b %d at %I:%M%p")}}</td> -->


from importjson import *


app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('homepage.html')

@app.route('/moviesShowing', methods=['POST'])
def my_form_post():
    # createPosterDatabase()

    start = request.form['startDate']
    numDays = request.form['numDays']
    zipcode = request.form['zipcode']
    zipcode = request.form['lat']
    zipcode = request.form['lng']
    daterange = request.form['radius']
    zipcode = request.form['units']

    # jsonData = getGracenoteAPI(startDate, numDays, zipcode, lat, lng, radius, units)
    jsonData = pullFromJson()

    if(jsonData == None):
        moviesShowing="Ran out of api calls"
    else:
        moviesShowing = (dumpToDatabase(jsonData))
    
    print(moviesShowing[0])
    print(type(moviesShowing[0]))

    return render_template("moviesShowing.html",moviesShowing=moviesShowing)

@app.route('/showtimes', methods=['POST'])
def returnMovieTimes():

    movieName = request.form['movie']
    alist = request.form.get('alist')
    dolby = request.form.get('Dolby')
    imax = request.form.get('Imax')

    times = searchDatabase(movieName, alist, dolby, imax)

    return render_template("showtimes.html",showtimes=times)
    

if __name__ == "__main__":
    app.run()