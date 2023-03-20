from flask import Flask, request, abort
from helpers.flask_file_upload import get_file_from_request
import json
from converters.title_converter import import_titles
from functionalities.total_minutes_watched import calculate_time_watched
from functionalities.pick_unwatched_title import pick_unwatched_title
from functionalities.movies_by_year import get_movie_by_rating_year_report, get_movie_by_release_year_report
from functionalities.most_watched_genres import get_most_watched_genres
from functionalities.most_favourite_genres import get_most_favourite_genres

app = Flask(__name__)
app.config.from_file("config.json", load=json.load)

def send_file_format_error():
    abort(400, "Invalid file format.")

def secure_import_titles(filename):
    try:
        return import_titles(filename)
    # if there is more fields than headers
    # if the file is not csv formatted
    except (TypeError, IndexError):
        send_file_format_error()

@app.route('/recommend', methods=['POST'])
def recommend_title_from_list():
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
        
@app.route('/time_watching', methods=['POST'])
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

@app.route('/report/movie/year', methods=['POST'])
def create_movie_report_by_year():
    separate_condition = request.args.get('separate_condition')
    if separate_condition is None:
        return 'No selected separate_condition', 400
    # RATE YEAR
    if separate_condition == "RATEY":
        report_generator = get_movie_by_rating_year_report
    # RELEASE YEAR
    elif separate_condition == "RELEASEY":
        report_generator = get_movie_by_release_year_report
    else:
        return 'Invalid by', 400
    filepath = get_file_from_request(app, allowed_extensions = ["csv"])
    titles = secure_import_titles(filepath)
    try:
        report = report_generator(titles)
    except (KeyError, ValueError):
        send_file_format_error()
    return json.dumps(report, indent=4, sort_keys=True)

@app.route('/report/movie/genre', methods=['POST'])
def create_movie_report_by_genre():
    filepath = get_file_from_request(app, allowed_extensions = ["csv"])
    titles = secure_import_titles(filepath)
    try:
        report = get_most_watched_genres(titles)
    except KeyError:
        send_file_format_error()
    return json.dumps(report, indent=4)

@app.route('/favourite/movie/genre', methods=['POST'])
def create_movie_report_by_favourite_genre():
    filepath = get_file_from_request(app, allowed_extensions = ["csv"])
    titles = secure_import_titles(filepath)
    try:
        report = get_most_favourite_genres(titles)
    except KeyError:
        send_file_format_error()
    return json.dumps(report, indent=4)

app.run()