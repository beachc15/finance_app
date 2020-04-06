from django.shortcuts import render
import pandas as pd
import json
import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime

from .forms import NameForm


def data_view(request):
    if request.method == 'POST':
        print('Post', request.POST['tickers'])
    try:
        tickers = request.POST['tickers']
        frequency = request.POST['frequency']
        period = request.POST['period']
        tickers = tickers.split(', ')


        remote_url = 'https://sleepy-garden-10843.herokuapp.com/api'

        j_data = json.dumps({'tickers': tickers, 'period': period,'frequency': frequency})
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        r = requests.post(remote_url, data=j_data, headers=headers)
        z = r.json()
        # print(z['matrix'])
        data = json.loads(z['matrix'])['data']
        stats = z['statistics']
        prices = stats['month_stats']['stat_prices']
        prices = pd.DataFrame(json.loads(prices))
        dates = list(map(int, prices.index))
        formatted_dates = []
        for date in dates:
            formatted_dates.append(datetime.utcfromtimestamp(float(date)/1000.).date())
        prices.insert(0, 'Dates', formatted_dates)
        df = pd.DataFrame(data)
        df = df.round(5)

        yearly_stats = stats['year_stats']
        year_series = pd.DataFrame({'average': json.loads(yearly_stats['average']), 'variance': json.loads(yearly_stats['variance']), 'Standard Deviation': json.loads(yearly_stats['simga'])})
        year_series = year_series.transpose()
        year_series.insert(0, 'index', ['Average', 'Variance', 'Std-dev'])

        monthly_stats = stats['month_stats']
        month_series = pd.DataFrame(
            {'average': json.loads(monthly_stats['average']), 'variance': json.loads(monthly_stats['variance']),
             'Standard Deviation': json.loads(monthly_stats['sigma'])})
        month_series = month_series.transpose()
        month_series.insert(0, 'index', ['Average', 'Variance', 'Std-dev'])

        gen_stats = json.loads(stats['stats'])['data']
        gen_stats = pd.DataFrame(gen_stats)
        for stat in json.loads(stats['stats']):
            print(stat)



        return render(request, 'varcovar/api.html', {'DataFrame': df, 'prices': prices, 'year_stats': year_series, 'month_stats': month_series, 'gen_stats': gen_stats})
    except ModuleNotFoundError:
        return render(request, 'varcovar/index.html', {'form': NameForm})


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            print('form is valid')
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'varcovar/index.html', {'form': form})
