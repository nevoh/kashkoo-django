import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import IncomeForm
from .models import Income


def incomes_view(request):
    return render(request, 'incomes/incomes.html')

def incomes_table(request):
    incomes = Income.objects.all()

    return render(request, 'incomes/incomes-table.html', {'incomes':incomes})


def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={
                'HX-Trigger': json.dumps({
                'incomesListChanged': None,
                'showSuccessMessage': 'Income added successfully'
                })
            })
    else:
        form = IncomeForm()
        

    return render(request, 'incomes/income-form.html', {'form':form})

def update_income(request, pk):
    income = get_object_or_404(Income, pk=pk)
    form = IncomeForm(instance=income)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204, headers={
                'HX-Trigger': json.dumps({
                'incomesListChanged': None,
                'showSuccessMessage': 'Income updated successfully'
                })
            })

    return render(request, 'incomes/income-form.html', {'form':form})

def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk)
    income.delete()
    return HttpResponse(status=204, headers={
                'HX-Trigger': json.dumps({
                'incomesListChanged': None,
                'showSuccessMessage': 'Income deleted successfully'
                })
            })
def get_growth_rate(a, p, t):
    """
    uses simple interest formula to calculate the rate of growth
    given the annual amount, expected amount after 65 years and
    the number of years
    """
    # simple interest formula --> A = P(1 + rt)
    r = (a - p) / (p*t)
    return r

def get_single_income_chart_values(pk):
    """
    This function returns a list of the y values 
    for the total income chart
    """
    single_income_values = []

    year = 1 # current income year
    growth_multiplyer = 1 # annual multiplyer factor for incomes with growth
    
    income = Income.objects.get(pk=pk)
    rate = get_growth_rate(income.growth, income.annual_amount, 65 - (income.start_age or 40))
    for i in range(40, 101): # selected range is because age is assumed from 40 to 100
        if i <= (income.end_age or 100) and i >= (income.start_age or 40):
            # append the income amount only if age iteration is between
            # the start and end age
            single_income_values.append(int(income.annual_amount * growth_multiplyer)) 

            if income.growth:
                # set the multiplyer factor given the current income year and growth rate
                growth_multiplyer = (1 + (rate * year))
        else:
            single_income_values.append(0)
        year = year + 1
    

    # return a sum of all the single income lists to get a total income list
    return single_income_values

def get_total_income_chart_values():
    """
    This function returns a list of the y values 
    for the total income chart
    """
    single_income_values = []
    total_income_values = []

    year = 1 # current income year
    growth_multiplyer = 1 # annual multiplyer factor for incomes with growth
    
    for income in Income.objects.all():
        rate = get_growth_rate(income.growth or 0, income.annual_amount, 65 - (income.start_age or 40))
        for i in range(40, 101): # selected range is because age is assumed from 40 to 100
            if i <= (income.end_age or 100) and i >= (income.start_age or 40):
                # append the income amount only if age iteration is between
                # the start and end age
                single_income_values.append(int(income.annual_amount * growth_multiplyer)) 

                if income.growth:
                    # set the multiplyer factor given the current income year and growth rate
                    growth_multiplyer = (1 + (rate * year))
            else:
                single_income_values.append(0)
            year = year + 1
        # siv meanse single_income_values [[siv1, siv2, ... sivn]] 
        total_income_values.append(single_income_values)

        single_income_values = []
        year = 1
        growth_multiplyer = 1
        print(total_income_values)
        print(growth_multiplyer)

    # return a sum of all the single income lists to get a total income list
    return [x + y for (x, y) in zip(*total_income_values)] 

def income_chart(request):
    pk = request.GET.get('pk')
    title = request.GET.get('title')
    if pk:
        y_values = get_single_income_chart_values(pk)
    else:
        y_values = get_total_income_chart_values()

    context = {
        'title':title,
        'y_values':y_values
    }
    return render(request, 'incomes/income-chart.html', context)





