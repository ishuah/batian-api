from django.shortcuts import redirect
from django.views.decorators.http import require_GET

@require_GET
def index(request): 
    return redirect('/api/v1')
