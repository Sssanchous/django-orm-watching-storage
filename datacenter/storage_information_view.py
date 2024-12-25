from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datetime import *
from django.utils.timezone import localtime


def get_duration(visit):
    if visit.leaved_at:
        delta = visit.leaved_at - visit.entered_at
    else:
        time_now = localtime()
        delta = time_now - visit.entered_at
    return delta


def format_duration(visit):
    total_seconds = int(visit.total_seconds())
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)

    return f'{hours:02}:{minutes:02}:{seconds:02}'


def storage_information_view(request):

    visits = Visit.objects.all()
    not_leaved_visits = Visit.objects.filter(leaved_at=None)

    non_closed_visits = []

    for visit in not_leaved_visits:
        owner_name = visit.passcard.owner_name
        entered_time = localtime(visit.entered_at)
        time_spent = get_duration(visit)

        non_closed_visits.append({
            'who_entered': owner_name,
            'entered_at': entered_time,
            'duration': format_duration(time_spent)
        })

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
