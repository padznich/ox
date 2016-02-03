from django import forms


class PlayerFilterEmailForm(forms.Form):

    email = forms.EmailField(label='Email filter ')

class PlayerChangeForm(forms.Form):

    xp = forms.IntegerField(label="Xp ")

class LogFilterForm(forms.Form):

    from_date = forms.DateField(label='From date', required=False)
    to_date = forms.DateField(label='To date', required=False)
    player_id = forms.IntegerField(label="Player ID", required=False)
