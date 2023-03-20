from flask import Flask, request
from helpers.flask_file_upload import get_file_from_request
import os
import json
from converters.title_converter import import_titles
from functionalities.total_minutes_watched import calculate_time_watched
from functionalities.pick_unwatched_title import pick_unwatched_title
from functionalities.movies_by_year import get_movie_by_rating_year_report, get_movie_by_release_year_report
from functionalities.most_watched_genres import get_most_watched_genres
from functionalities.most_favourite_genres import get_most_favourite_genres

app = Flask(__name__)
app.config.from_file("config.json", load=json.load)

@app.route('/recommend', methods=['POST'])
def recommend_title_from_list():
    filepath = get_file_from_request(app, allowed_extensions = ["csv"])
    titles = import_titles(filepath)
    picked_title = pick_unwatched_title(titles)
    response = {
        'title': picked_title["Title"],
        'directors': picked_title["Directors"],
        'year': picked_title["Year"],
        'imdb link': picked_title["URL"]
    }
    os.remove(filepath)
    return json.dumps(response, indent=4)

@app.route('/time_watching', methods=['POST'])
def get_total_minutes():
    filepath = get_file_from_request(app, allowed_extensions = ["csv"])
    titles = import_titles(filepath)
    days, hours, minutes, total_minutes = calculate_time_watched(titles)
    response = {
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'total_minutes': total_minutes
        }
    os.remove(filepath)
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
    titles = import_titles(filepath)
    report = report_generator(titles)
    os.remove(filepath)
    return json.dumps(report, indent=4, sort_keys=True)

@app.route('/report/movie/genre', methods=['POST'])
def create_movie_report_by_genre():
    filepath = get_file_from_request(app, allowed_extensions = ["csv"])
    titles = import_titles(filepath)
    report = get_most_watched_genres(titles)
    os.remove(filepath)
    return json.dumps(report, indent=4)

@app.route('/favourite/movie/genre', methods=['POST'])
def create_movie_report_by_favourite_genre():
    filepath = get_file_from_request(app, allowed_extensions = ["csv"])
    titles = import_titles(filepath)
    report = get_most_favourite_genres(titles)
    os.remove(filepath)
    return json.dumps(report, indent=4)

app.run()

