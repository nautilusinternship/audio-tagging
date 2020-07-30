# --------------------------------------------------------
# app.py: app layer program for Audio Tagging application
# --------------------------------------------------------

from flask import Flask, request, redirect, make_response, render_template
# uncomment this to use db
from database import Audio_Params

app = Flask(__name__)


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

    audio_embed = createEmbed("spotify:track:6XkuklKiHYVTlVvWlTgQYP")
    html = render_template('index.html', audio_embed=audio_embed, song_info="Erase Me:Kid Cudi")
    response = make_response(html)
    return response


# https://www.tutorialspoint.com/flask/flask_sending_form_data_to_template.htm
@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'POST':
        result = request.form
        params = []
        title = ""
        artist = ""
        for r in result:
            val = result[r]
            # convert values from string to float
            if r != 'song_info':
                val = float(val)
                params.append(val)
            else:
                val = val.split(':')
                title = val[0]
                artist = val[1]
        print(title)
        print(artist)
        # uncomment this to add to db
        entry = Audio_Params().update_row(title, params)
    return render_template("results.html", result=result)


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
