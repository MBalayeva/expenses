from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from .models import UserPreferences
import os
import json

# Create your views here.
def index(request):
    user_preference = UserPreferences.objects.get(user=request.user)

    currencies = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_data:
        data = json.load(json_data)

        for k, v in data.items():
            currencies.append({'name': k, 'value': v})

    context = {
        'currencies': currencies
    }

    if request.method == "GET":
        return render(request, 'userpreferences/index.html', context)

    else: 
        currency = request.POST['currency']
        user_preference.currency = currency
        user_preference.save()
        messages.success(request, 'Changes saved')

        return render(request, 'userpreferences/index.html', context)

