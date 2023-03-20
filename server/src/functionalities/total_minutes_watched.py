from functionalities.title_filter import filter_movies

def get_days_hours_minutes(total_minutes):
    days = int(total_minutes / 1440)
    rest_minutes = int(total_minutes % 1440)
    hours = int(rest_minutes / 60)
    minutes = total_minutes - (days*1440) - (hours*60)
    return days, hours, minutes

# returns days, hours and minutes
def calculate_time_watched(titles):
    ratings = filter_movies(titles)
    total_minutes = sum(map(lambda r: int(r['Runtime (mins)']), ratings))
    days, hours, minutes = get_days_hours_minutes(total_minutes)
    return days, hours, minutes, total_minutes