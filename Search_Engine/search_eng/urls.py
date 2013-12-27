
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('search_eng.views',
    url(r'^search_eng/$', 'CheckUrl', name='check_url'),
    url(r'^index_view/(?P<index_pk>\d+)$', 'index_view', name='index_view'),
    url(r'^query_view/(?P<index_pk>\d+)$', 'query_view', name='query_view'),
    url(r'^$', 'CheckUrl', name='check_url')

)