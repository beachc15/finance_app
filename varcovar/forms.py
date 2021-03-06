from django import forms

period_choices = (
    ('10y', 'Ten Years'),
    ('3mo', 'Three Months'),
    ('6mo', 'Six-Months'),
    ('1y', 'One Year'),
    ('2y', 'Two Years'),
    ('5y', 'Five Years'),

    ('ytd', 'Year-To-Date'),
    ('max', 'Maximum Time')
)

freq_choices = (
    ('1mo', 'Monthly'),
    ('1d', 'Daily'),
    ('1wk', 'Weekly'),
    ('3mo', 'Three Months')
)


class NameForm(forms.Form):
    tickers = forms.CharField(label='tickers', max_length=100)
    period = forms.ChoiceField(choices=period_choices, label='period')
    frequency = forms.ChoiceField(choices=freq_choices, label='frequency')
