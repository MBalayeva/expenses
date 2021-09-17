from django.shortcuts import render
from django.conf import settings
import os
import json

# Create your views here.
def index(request):
    currencies = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    return render(request, 'userpreferences/index.html')