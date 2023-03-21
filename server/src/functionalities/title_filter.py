def filter_by_title_type(titles, title_type):
    return list(filter(lambda t: t['Title Type'] == title_type, titles))

def filter_movies(titles):
    return filter_by_title_type(titles, 'movie')