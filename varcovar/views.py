from django.shortcuts import render
import pandas as pd
import json
import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm


def data_view(request):
    if request.method == 'POST':
        print('Post', request.POST['tickers'])
    try:
        tickers = request.POST['tickers']
        frequency = request.POST['frequency']
        period = request.POST['period']


        print(frequency)
        print(period)

        remote_url = 'https://sleepy-garden-10843.herokuapp.com/api'

        j_data = json.dumps({'tickers': tickers, 'period': period,'frequency': frequency})
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        r = requests.post(remote_url, data=j_data, headers=headers)
        z = r.json()
        df = pd.DataFrame(z['data'])
        df = df.round(5)
        return render(request, 'varcovar/api.html', {'DataFrame': df})
    except:
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
