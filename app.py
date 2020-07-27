# --------------------------------------------------------
# app.py: app layer program for Audio Tagging application
# --------------------------------------------------------

from flask import Flask, request, redirect, make_response, render_template
app = Flask(__name__)
# uncomment this to use db
from database import Audio_Params

# index/home view
@app.route('/')
def index():
    # embed audio clip to be played
    # display input fields
    # redirect to confirmation view
    html = render_template('index.html')
    response = make_response(html)
    return response

# https://www.tutorialspoint.com/flask/flask_sending_form_data_to_template.htm
@app.route('/results',methods = ['POST', 'GET'])
def results():
    # this will just show ur results on the webpage
    if request.method == 'POST':
        result = request.form
        params = []
        title = ""
        for r in result:
            val = result[r]
            # convert values from string to float
            if r != 'title':
                val = float(val)
                params.append(val)
            else:
                title = val
        # uncomment this to add to db
        entry = Audio_Params().add_row(title, params)
    return render_template("results.html",result = result)


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
