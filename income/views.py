from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Income, Source
from userpreferences.models import UserPreferences
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.http import JsonResponse


def search_income(request):
    search_str = request.POST.get('searchText')

    income = Income.objects.filter(
        amount__istartswith=search_str, owner=request.user) | Income.objects.filter(
        date__istartswith=search_str, owner=request.user) | Income.objects.filter(
        description__icontains=search_str, owner=request.user) | Income.objects.filter(
        source__icontains=search_str, owner=request.user)
    
    data = income.values()
    return JsonResponse(list(data), safe=False)


@login_required(login_url='authentication/login')
def index(request):
    income = Income.objects.filter(owner=request.user)
    preference = UserPreferences.objects.get(user=request.user)

    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': preference.currency
    }
    return render(request, 'income/index.html', context)


def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        income_date = request.POST['income_date']

        if not amount:
            messages.error(request, 'Fill in the amount field')
            return render(request, 'income/add_income.html', context)

        if not description:
            messages.error(request, 'Fill in the description field')
            return render(request, 'income/add_income.html', context)

        if not income_date:
            Income.objects.create(owner=request.user, amount=amount, description=description, source=source,)
        else: Income.objects.create(owner=request.user, amount=amount, description=description, source=source, date=income_date)
         
        messages.success(request, "Income added successfully")
        return redirect('income')


def edit_income(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all
    context = {
        'income': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit-income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        source = request.POST['source']
        income_date = request.POST['income_date']

        if not amount:
            messages.error(request, 'Fill in the amount field')
            return render(request, 'income/edit-income.html', context)

        if not description:
            messages.error(request, 'Fill in the description field')
            return render(request, 'income/edit-income.html', context)

        income.owner = request.user
        income.amount = amount
        income.description = description
        income.source = source

        if not income_date:
            income.save()
        else: income.date = income_date

        income.save()
         
        messages.success(request, "Income updated successfully")
        return redirect('income')


class IncomeDeleteView(DeleteView):
    model = Income
    success_url = reverse_lazy('income')

