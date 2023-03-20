import csv

def import_titles(file_path):
    ratings = []

    with open(file_path, newline='', encoding="utf-8") as csvfile:
        file_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # get the headers
        headers = next(file_reader)
        for registry in file_reader:
            rating = {}
            # create the dict with all the headers and values
            for i in range(0,len(registry)):
                rating[ headers[i] ] = registry[i]
            ratings.append(rating)
    return ratings