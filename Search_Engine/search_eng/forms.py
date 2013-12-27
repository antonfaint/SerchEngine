from django import forms

class Query_Form( forms.Form ):
    depth = forms.IntegerField(max_value=3)
    url = forms.URLField()

class Answer_Form( forms.Form ):
    query = forms.CharField(max_length=100)