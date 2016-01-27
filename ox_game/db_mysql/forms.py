from django import forms

class PlayerChangeForm(forms.Form):

    xp = forms.IntegerField(label='Xp')
