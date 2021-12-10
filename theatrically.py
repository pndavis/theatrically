from flask import Flask, request, render_template
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from importjson import *


app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/moviesShowing', methods=['POST'])
def my_form_post():
    start = '&startDate=' + request.form['start']
    numDays = '&numDays' + request.form['numDays']
    zipcode = '&zip=' + request.form['zip']
    daterange = '&radius' + request.form['range']

    # jsonData = getGracenoteAPI(start, numDays, zipcode, daterange)
    jsonData = pullFromJson()

    if(jsonData == None):
        moviesShowing="Ran out of api calls"
    else:
        moviesShowing = (dumpToDatabase(jsonData))
        # moviesShowingSorted = sorted((moviesShowing), key=str.casefold)
        
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