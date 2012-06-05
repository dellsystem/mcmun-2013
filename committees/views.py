from django.shortcuts import render
from django.http import Http404
from committees.models import Committee

def view(request, slug):
    try:
        committee = Committee.objects.get(slug=slug)
    except Committee.DoesNotExist:
        raise Http404

    data = {
        'committee': committee,
    }

    return render(request, 'committee.html', data)
