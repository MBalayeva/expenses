from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense, Category
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.core.paginator import Paginator
from django.http import JsonResponse
from userpreferences.models import UserPreferences
import datetime
from django.utils.timezone import make_aware

def search_expenses(request):
    search_str = request.POST.get('searchText')

    expenses = Expense.objects.filter(
        amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
        date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
        description__icontains=search_str, owner=request.user) | Expense.objects.filter(
        category__icontains=search_str, owner=request.user)
    
    data = expenses.values()
    return JsonResponse(list(data), safe=False)


# Create your views here.
@login_required(login_url='authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    preference = UserPreferences.objects.get(user=request.user)

    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': preference.currency
    }
    return render(request, 'expenses/index.html', context)


def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expenses.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        expense_date = request.POST['expense_date']


        if not amount:
            messages.error(request, 'Fill in the amount field')
            return render(request, 'expenses/add_expenses.html', context)

        if not description:
            messages.error(request, 'Fill in the description field')
            return render(request, 'expenses/add_expenses.html', context)

        if not expense_date:
            Expense.objects.create(owner=request.user, amount=amount, description=description, category=category,)
        else: Expense.objects.create(owner=request.user, amount=amount, description=description, category=category, date=expense_date)
         
        messages.success(request, "Expense added successfully")
        return redirect('expenses')


def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all
    context = {
        'expense': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        expense_date = request.POST['expense_date']


        if not amount:
            messages.error(request, 'Fill in the amount field')
            return render(request, 'expenses/edit-expenses.html', context)

        if not description:
            messages.error(request, 'Fill in the description field')
            return render(request, 'expenses/edit-expenses.html', context)
        expense.owner = request.user
        expense.amount = amount
        expense.description = description
        expense.category = category
        if not expense_date:
            expense.save()
        else: expense.date = expense_date

        expense.save()
         
        messages.success(request, "Expense updated successfully")
        return redirect('expenses')


class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = reverse_lazy('expenses')


def expenses_summary(request):
    current_date = datetime.date.today()
    six_month_period = datetime.timedelta(days=30*6)      
    six_month_ago = current_date - six_month_period

    expenses = Expense.objects.filter(owner=request.user, date__gte=six_month_ago, date__lte=current_date)
    finalrep = {}

    def get_categories(expense):
        return expense.category

    def get_amount(category):
        amount = 0
        expenses_for_category = expenses.filter(category=category)

        for expense in expenses_for_category:
            amount += expense.amount

        return amount

    categories = list(set(map(get_categories, expenses))) 

    for c in categories:
        finalrep[c] = get_amount(c)

    return JsonResponse(finalrep)


def statsView(request):
    if request.method == "GET":
        return render(request, 'expenses/stats.html')