from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Expense, Category

# Create your views here.
@login_required(login_url='authentication/login')
def index(request):
    return render(request, 'expenses/index.html')


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


