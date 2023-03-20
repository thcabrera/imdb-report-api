from flask import Flask, abort
from helpers.flask_file_upload import get_file_from_request
import json
import os
from converters.title_converter import import_titles
from functionalities.total_minutes_watched import calculate_time_watched
from functionalities.pick_unwatched_title import pick_unwatched_title
from functionalities.movies_by_year import get_movie_by_rating_year_report, get_movie_by_release_year_report
from functionalities.most_watched_genres import get_most_watched_genres
from functionalities.most_favourite_genres import get_most_favourite_genres

app = Flask(__name__)

def send_file_format_error():
    abort(400, "Invalid file format.")

def secure_import_titles(filename):
    try:
        return import_titles(filename)
    # if there is more fields than headers
    # if the file is not csv formatted
    except (TypeError, IndexError):
        send_file_format_error()

# RESOURCE "MOVIES"

@app.route('/movies/picku', methods=['POST'])
def pick_unwatched_movie_from_list():
    filepath = get_file_from_request(app, allowed_extensions = ["csv"])
    titles = secure_import_titles(filepath)
    try:
        picked_title = pick_unwatched_title(titles)
        response = {
        'title': picked_title["Title"],
        'directors': picked_title["Directors"],
        'year': picked_title["Year"],
        'imdb link': picked_title["URL"]
        }
        return json.dumps(response, indent=4)
    except KeyError:
        send_file_format_error()
        
@app.route('/movies/time', methods=['POST'])
def get_total_minutes():
    filepath = get_file_from_request(app, allowed_extensions = ["csv"])
    titles = secure_import_titles(filepath)
    try:
        days, hours, minutes, total_minutes = calculate_time_watched(titles)
    except KeyError:
        send_file_format_error()
    response = {
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'total_minutes': total_minutes
        }
    return json.dumps(response, indent=4).decode("utf-16")

@app.route('/movies/yreleased', methods=['POST'])
def create_movie_report_by_year_released():
    filepath = get_file_from_request(app, allowed_extensions = ["csv"])
    titles = secure_import_titles(filepath)
    try:
        report = get_movie_by_rating_year_report(titles)
    except (KeyError, ValueError):
        send_file_format_error()
    return json.dumps(report, indent=4, sort_keys=True)

@app.route('/movies/yrated', methods=['POST'])
def create_movie_report_by_year_rated():
    filepath = get_file_from_request(app, allowed_extensions = ["csv"])
    titles = secure_import_titles(filepath)
    try:
        report = get_movie_by_rating_year_report(titles)
    except (KeyError, ValueError):
        send_file_format_error()
    return json.dumps(report, indent=4, sort_keys=True)

@app.route('/movies/genre/mw', methods=['POST'])
def create_movie_report_by_most_watched_genre():
    filepath = get_file_from_request(app, allowed_extensions = ["csv"])
    titles = secure_import_titles(filepath)
    try:
        report = get_most_watched_genres(titles)
    except KeyError:
        send_file_format_error()
    return json.dumps(report, indent=4)

@app.route('/movies/genre/fav', methods=['POST'])
def create_movie_report_by_favourite_genre():
    filepath = get_file_from_request(app, allowed_extensions = ["csv"])
    titles = secure_import_titles(filepath)
    try:
        report = get_most_favourite_genres(titles)
    except KeyError:
        send_file_format_error()
    return json.dumps(report, indent=4)

app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))