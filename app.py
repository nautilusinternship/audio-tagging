# --------------------------------------------------------
# app.py: app layer program for Audio Tagging application
# --------------------------------------------------------

from flask import Flask, request, redirect, make_response, render_template
app = Flask(__name__)

# index/home view
@app.route('/')
def index():
    # embed audio clip to be played
    # display input fields
    # redirect to confirmation view
    html = render_template('index.html')
    response = make_response(html)
    return response

# confirmation view
@app.route('/success')
def success():
    # parse user inputs as list
    descriptors = request.form.getlist('input')
    # send descriptors to db layer file to be manipulated/to update db

    # display confirmation message to verify success of user inputs being processed
    # view will maybe have a button to return home to repeat process on another audio file?
    html = render_template('success.html')
    response = make_response(html)
    return response

if __name__ == "__main__":
    app.run()
