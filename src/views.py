from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from aligner.forms import UploadFileForm

def handle_uploaded_file(f):

    for chunk in f.chunks():
        pass


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_source_file = request.FILES['source_file']
            new_target_file = request.FILES['target_file']
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render_to_response('aligner/upload.html', {'form': form})
