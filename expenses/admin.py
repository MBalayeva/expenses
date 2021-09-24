from django.contrib import admin
from .models import Expense, Category

# Register your models here.
admin.site.register(Expense)
admin.site.register(Category)

class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'date', 'category', 'owner')
    search_fields = ('description', 'category')
