from datetime import datetime
from functionalities.title_filter import filter_movies

def get_rating_year(rating):
    return rating['Date Rated'].year

def get_release_year(rating):
    return rating['Year']

def process_rating_by_release_year(ratings_by_release_year, rating, get_year):
    release_year = get_year(rating)
    if release_year not in ratings_by_release_year:
        ratings_by_release_year[release_year] = []
    ratings_by_release_year[release_year].append(rating)

def separate_by_release_year(ratings, get_year):
    ratings_by_release_year = {}
    for rating in ratings:
        process_rating_by_release_year(ratings_by_release_year, rating, get_year)
    return ratings_by_release_year

def create_json_format(ratings_by_year):
    json_data = {}
    for year in ratings_by_year:
        json_data[year] = {}
        json_data[year]['total'] = len(ratings_by_year[year])
        json_data[year]['ratings'] = list(map(lambda r: r['Title'], ratings_by_year[year]))
    return json_data

# GENERIC FUNCTION
def get_movies_by_year_report(titles, get_year):
    movie_ratings = filter_movies(titles)
    return create_json_format(separate_by_release_year(movie_ratings, get_year))

def get_movie_by_rating_year_report(titles):
    movie_ratings = filter_movies(titles)
    return create_json_format(separate_by_release_year(movie_ratings, get_rating_year))

def get_movie_by_release_year_report(titles):
    movies = filter_movies(titles)
    return create_json_format(separate_by_release_year(movies, get_release_year))