import random

def get_unwatched_titles(titles):
    return list(filter(lambda t: t["Your Rating"] is None, titles))

def pick_unwatched_title(titles):
    unwatched_titles = get_unwatched_titles(titles)
    try:
        return random.choice(unwatched_titles)
    except IndexError:
        # if titles is not empty -> user passed list of already watched movies
        if titles != []:
            return None
        # if titles is empty -> user passed empty file
        raise IndexError