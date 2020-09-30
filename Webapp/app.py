
#Imports
import funcmap
from flask import Flask, render_template, url_for, request

#initializing the flask app
app = Flask('funcMap')

#Initializing the first page
@app.route("/")

# Initializing and Defining what happens on the home page
@app.route("/home")
def home():
    return render_template('home.html')


# Initializing and Defining what happens on the about page
@app.route("/about")
def about():
    return render_template('about.html')

# Initializing and Defining what happens on the results page
@app.route("/results")
def results():
    return render_template('results.html')


# Initializing and Defining what happens when someone clicks submit
@app.route("/submit")
def form_submit():
    user_input = request.args
    search = str(user_input['search'])
    event = str(user_input['event'])
    response = str(user_input['emergencyinput']) # get the user input
    if search == "strict":
        output = funcmap.map_strict(response, event)
    elif search == "loose":
        output = funcmap.map_loose(response, event)
    return render_template('results.html', output1 = output) # Show html output on page



if __name__ == '__main__':
    app.run(debug=True)
