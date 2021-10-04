from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="income"),   
    path('add-income/', views.add_income, name="add-income"),
    path('edit-income/<int:id>/', views.edit_income, name="edit-income"),
    path('delete-income/<int:pk>', views.IncomeDeleteView.as_view(), name="delete-income"),
    path("search-income/", views.search_income, name="search-income"),
    path('stats-income/', views.IncomeSummaryView, name="stats-income"),
    path('income-summary', views.income_summary)
]