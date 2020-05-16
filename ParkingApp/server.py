from flask import *
from search import *
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# app = Flask(__name__)


# @app.route("/")
# def home():
#     if device_known():
#         print("----====----===---this is the user id for this session goes to index" + session['user_id'])
#         return app.send_static_file("index.html")
#     else:
#         print("----====----===---this is the user id for this session goes to signup" + session['user_id'])
#         return app.send_static_file("signup.html")


def device_known():
    if session['user_id'] is not None:
        return True # check in cache
    else:
        return False


@app.route("/search")
def search():
    """
    This page will contain the search result from the database.
    :return:
    """
    return render_template("car_search_results.html")


@app.route("/signup")
def email_form():
    return app.send_static_file("signup.html")


# app.run(debug=True)
