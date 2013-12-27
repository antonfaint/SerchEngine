from django.conf.urls import patterns, url

urlpatterns = patterns('aligner.views',
    url(r'^$', 'aligner.views.upload_file', name='list'),
)