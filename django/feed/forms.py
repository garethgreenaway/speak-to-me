from django import forms

class AddFeedForm(forms.Form):
    url = forms.URLField(label='Feed URL')
