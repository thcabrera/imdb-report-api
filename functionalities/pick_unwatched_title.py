import random

def get_unwatched_titles(titles):
    return list(filter(lambda t: t["Your Rating"] == "", titles))

def pick_unwatched_title(titles):
    unwatched_titles = get_unwatched_titles(titles)
    return random.choice(unwatched_titles)