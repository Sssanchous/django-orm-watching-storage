from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime


def is_visit_long(visit, seconds=3600):
    if visit.leaved_at:
        delta_seconds = (visit.leaved_at - visit.entered_at).total_seconds()
        if delta_seconds > seconds:
            return True
    else:
        delta_seconds = get_duration(visit).total_seconds()
        if delta_seconds > seconds:
            return True
    return False


def get_duration(visit):
    if visit.leaved_at:
        delta = visit.leaved_at - visit.entered_at
    else:
        time_now = localtime()
        delta = time_now - visit.entered_at
    return delta


def format_duration(duration):
    total_seconds = int(duration.total_seconds())  
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)

    return f'{hours:02}:{minutes:02}:{seconds:02}'


def passcard_info_view(request, passcode):

    passcard = get_object_or_404(Passcard, passcode=passcode)

    visits = Visit.objects.filter(passcard=passcard)

    this_passcard_visits = []

    for visit in visits:
        time_spent = get_duration(visit)

        this_passcard_visits.append({
            'entered_at': visit.entered_at,
            'duration': format_duration(time_spent),
            'is_strange': is_visit_long(visit)
        })

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
