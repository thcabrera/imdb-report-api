import csv
from datetime import datetime

class DataFormatError(Exception):
    pass

# converts a string to a datetime with the format YYYY-MM-DD
def convert_to_datetime(s):
    return datetime.strptime(s,'%Y-%m-%d')

# applies the converter to the value. if an exception is raised,
# it will check if the value is the empty string "" and if it can be None,
# and will return None if True, otherwise will raise DataFormatError
def convert_value(value, converter, nullable = False):
    try:
        return converter(value)
    except Exception:
        if value != "" or not nullable:
            raise DataFormatError
        return None

def import_from_list(reg):
    return {
        "Position": int(reg[0]),
        "Const": reg[1],
        "Created": convert_value(reg[2], convert_to_datetime, False),
        "Modified": convert_value(reg[3], convert_to_datetime, False),
        "Description": reg[4],
        "Title": reg[5],
        "URL": reg[6],
        "Title Type": reg[7],
        "IMDb Rating": float(reg[8]),
        "Runtime (mins)": convert_value(reg[9], int, True),
        "Year": int(reg[10]),
        "Genres": list(map(lambda g: g.strip(), reg[11].split(','))),
        "Num Votes": reg[12],
        "Release Date": convert_value(reg[13], convert_to_datetime, False),
        "Directors": list(map(lambda g: g.strip(), reg[14].split(','))),
        "Your Rating": convert_value(reg[15], int, True),
        "Date Rated": convert_value(reg[16], convert_to_datetime, True)
    }

def import_from_ratings(reg):
    return {
        "Const": reg[0],
        "Your Rating": int(reg[1]),
        "Date Rated": convert_value(reg[2], convert_to_datetime, False),
        "Title": reg[3],
        "URL": reg[4],
        "Title Type": reg[5],
        "IMDb Rating": float(reg[6]),
        "Runtime (mins)": convert_value(reg[7], int, True),
        "Year": int(reg[8]),
        "Genres": list(map(lambda g: g.strip(), reg[9].split(','))),
        "Num Votes": reg[10],
        "Release Date": convert_value(reg[11], convert_to_datetime, False),
        "Directors": list(map(lambda g: g.strip(), reg[12].split(',')))
    }

def import_titles(file_path):
    try:
        ratings = []

        with open(file_path, newline='', encoding="utf-8") as csvfile:
            file_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            # skip the headers
            headers = next(file_reader)
            if headers[0] == "Position":
                import_func = import_from_list
            else:
                import_func = import_from_ratings
            for registry in file_reader:
                rating = import_func(registry)
                ratings.append(rating)
        return ratings
    except (TypeError, IndexError, KeyError, ValueError) as e:
        raise DataFormatError