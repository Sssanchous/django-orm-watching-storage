from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datetime import *
from django.utils.timezone import localtime
from .visit_duration_utils import get_duration, format_duration


def storage_information_view(request):

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
