from functionalities.title_filter import filter_movies

def separate_by_genre(movies):
    movies_by_genre = {} # genre -> list of movies
    for movie in movies:
        # 'Action, Adventure' -> split(',') -> ['Action',' Adventure'] -> strip() -> ['Action','Adventure']
        genres = list(map(lambda g: g.strip(), movie['Genres'].split(',')))
        genres_and_comb = list(map(lambda g: str(g), get_all_sublists(genres)))
        for genre in genres_and_comb:
            if genre not in movies_by_genre:
                movies_by_genre[genre] = 0
            movies_by_genre[genre] += 1
    return movies_by_genre

# TODO SOLUCIONAR ESTO, NO ESTA HACIENDO LO QUE QUIERO
def sort_result(movies_by_genre):
    sorted_keys = sorted(movies_by_genre, key = lambda g: movies_by_genre[g], reverse = True)
    sorted_dict = {}
    for sorted_key in sorted_keys:
        sorted_dict[sorted_key] = movies_by_genre[sorted_key]
    return sorted_dict

def get_most_watched_genres(titles):
    movies = filter_movies(titles)
    movies_by_genre = separate_by_genre(movies)
    # sort by total movies
    return sort_result(movies_by_genre)

def get_all_sublists(A): 
    # store all the sublists  
    B = [[ ]]
    # first loop  
    for i in range(len(A) + 1):   
        # second loop  
        for j in range(i + 1, len(A) + 1):
            # slice the subarray  
            sub = A[i:j] 
            B.append(sub)
    B.remove([])
    return B