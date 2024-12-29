from django.utils.timezone import localtime


def get_duration(visit):

    time_now = localtime()

    if visit.leaved_at:
        delta = visit.leaved_at - visit.entered_at
    else:
        delta = time_now - visit.entered_at
    return delta


def format_duration(duration, seconds_in_hour = 3600, seconds_in_minute = 60):

    total_seconds = int(duration.total_seconds())
    hours = total_seconds // seconds_in_hour
    minutes = (total_seconds % seconds_in_hour) // seconds_in_minute
    seconds = total_seconds % seconds_in_minute
    return f'{hours:02}:{minutes:02}:{seconds:02}'


def is_visit_long(visit, seconds_in_hour = 3600):
    if visit.leaved_at:
        delta_seconds = (visit.leaved_at - visit.entered_at).total_seconds()
    else:
        delta_seconds = get_duration(visit).total_seconds()
    return delta_seconds > seconds_in_hour