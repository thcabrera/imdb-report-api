def filter_by_title_type(ratings, title_type):
    return list(filter(lambda r: r['Title Type'] == title_type, ratings))

def filter_movies(ratings):
    return filter_by_title_type(ratings, 'movie')