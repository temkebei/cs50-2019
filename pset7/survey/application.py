import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request


# Configure application
app = Flask(__name__)


# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# This application directs the user to the form page once the website is clicked on


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")

# This loads the actual form.html page


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


""" This ensures that if any of the inputs are empty, an error page and message is returned.
If the client side validation does not work, and if JavaScript is disabled for instance, this will provide a back up validation.
If everything is correct the inputted data is written to a csv file. """


@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("firstName"):
        return render_template("error.html", message="You must state your first name.")
    if not request.form.get("lastName"):
        return render_template("error.html", message="You must state your last name.")
    if not request.form.get("title"):
        return render_template("error.html", message="You must state your title.")
    if not request.form.get("position"):
        return render_template("error.html", message="You must state your position.")
    if not request.form.get("email"):
        return render_template("error.html", message="You must provide your email address.")
    with open("survey.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow((request.form.get("firstName"), request.form.get("lastName"), request.form.get("title"),
                         request.form.get("position"), request.form.get("email")))
    return redirect("/sheet")


""" This reads the csv file when the site is directed towards /sheet and saves the data to a list called workers.
It then directs the site to sheet.html and assigns the workers list to a list local to sheet.html """


@app.route("/sheet")
def get_sheet():
    with open("survey.csv", "r") as file:
        reader = csv.reader(file)
        workers = list(reader)
    return render_template("sheet.html", workers=workers)
