from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime
from .visit_duration_utils import get_duration, format_duration, is_visit_long


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
