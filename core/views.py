from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.serializers import serialize

import json

from .models import Map

def index(request):
    maps = Map.objects.all()
    context = {'maps': maps}
    return render(request, 'core/index.html', context)

def read(request, map_id):
    m = get_object_or_404(Map, pk=map_id)
    return HttpResponse(serialize("json", m.layer_set.all()))
