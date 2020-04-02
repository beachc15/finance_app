from django import forms


class NameForm(forms.Form):
    tickers = forms.CharField(label='tickers', max_length=100)
