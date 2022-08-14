from django.urls import path

from . import views

urlpatterns = [
    path('', views.incomes_view, name='incomes'),
    path('incomes-table', views.incomes_table, name='incomes-table'),
    path('add-income', views.add_income, name='add-income'),
    path('update-income/<str:pk>', views.update_income, name='update-income'),
    path('delete-income/<str:pk>', views.delete_income, name='delete-income'),
    path('income-chart', views.income_chart, name='income-chart'),
]
