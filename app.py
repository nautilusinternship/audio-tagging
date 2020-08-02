# --------------------------------------------------------
# app.py: app layer program for Audio Tagging application
# --------------------------------------------------------

from flask import Flask, request, redirect, make_response, render_template
# uncomment this to use db
from database import Audio_Params
import csv
import random

app = Flask(__name__)


def getRandomSong():
    with open('test1doc.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # lines= len(list(readCSV))
        chosen_row = random.choice(list(readCSV))

    return {"song_info": chosen_row[0] + ":" + chosen_row[1], "uri": chosen_row[2]}


def parseURI(uri):
    uri = uri.split(":")
    if uri[1] != "track":
        print("error: this is not a track")
    else:
        return uri[len(uri) - 1]


def createEmbed(uri):
    return "https://open.spotify.com/embed/track/" + parseURI(uri)


# index/home view
@app.route('/')
def index():
    # embed audio clip to be played
    # display input fields
    # redirect to confirmation view
    song = getRandomSong()
    audio_embed = createEmbed("spotify:track:7ytR5pFWmSjzHJIeQkgog4")
    html = render_template('index.html', audio_embed=audio_embed, song_info=parseURI("spotify:track:7ytR5pFWmSjzHJIeQkgog4") + ":" + " ROCKSTAR (feat. Roddy Ricch): DaBaby")
    response = make_response(html)
    return response


# https://www.tutorialspoint.com/flask/flask_sending_form_data_to_template.htm
@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'POST':
        result = request.form.to_dict()
        uri = ""
        title = ""
        artist = ""
        for r in result:
            # convert values from string to float
            if r != 'song_info':
                result[r] = float(result[r])
            else:
                val = result[r].split(':')
                uri = val[0]
                title = val[1]
                artist = val[2]
        print(uri)
        print(title)
        print(artist)
        # Do this some other way
        # params.append(0)
        print(result)
        # uncomment this to add to db
        entry = Audio_Params().update_row(uri, result)
    return render_template("results.html", result=result, artist=artist, title=title)


# confirmation view
@app.route('/success')
def success():
    # parse user inputs as list
    # descriptors = request.form.getlist('input')
    # send descriptors to db layer file to be manipulated/to update db

    # display confirmation message to verify success of user inputs being processed
    # view will maybe have a button to return home to repeat process on another audio file?
    # html = render_template('success.html')
    # response = make_response(html)
    # return response
    return 'success'


if __name__ == "__main__":
    app.run()
