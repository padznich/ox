from django import forms

class PlayerChangeForm(forms.Form):

    xp = forms.IntegerField(label='Xp')

class LogDateFilterForm(forms.Form):

    from_date = forms.DateField(label='From date')
    to_date = forms.DateField(label='To date')