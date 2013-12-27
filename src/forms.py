from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    source_file  = forms.FileField()
    target_file  = forms.FileField()
