from django import forms

class Query_form( forms.Form ):

    url = forms.URLField()

class Answer_form( forms.Form ):
    query = forms.CharField(max_length=100)