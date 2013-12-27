from annoying.decorators import render_to
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import Query_Form, Answer_Form
from models import Index_Model
from search_eng.search_engine import Query_run, Create_index_from_url


class Index_Item_Data():
    def __init__(self, url, data_index):
        self.url = url

@render_to( 'search_eng/index_view.html' )
def Index_view( request, index_pk ):

    object_list = Index_Model.objects.all()
    return { 'object_list': object_list }

def CheckUrl( request ):

    if request.method == 'POST':
        form = Query_Form( request.POST )
        if form.is_valid():
            data =  Create_index_from_url( form.cleaned_data[ 'url' ] ,
                                           form.cleaned_data[ 'depth' ]
            )

            new_index = Index_Model.objects.create( index_url=form.cleaned_data[ 'url' ], index_data= data)
            new_index.save()
            return redirect( 'query_view', index_pk = new_index.pk )
    else:
        form = Query_Form()
    return render_to_response(
        "search_eng/new_index.html",
        { 'form': form },
        context_instance=RequestContext(request)
        )

@render_to( 'search_eng/query_view.html' )
def query_view(request, index_pk):

    if request.method == 'POST':
        form = Answer_Form( request.POST )
        if form.is_valid(  ):
            index = Index_Model.objects.filter( id = index_pk)[0]
            object_list = Query_run( form.cleaned_data['query'], index.index_data )
            return   { 'object_list': object_list , 'form':form }
    else:
        form = Answer_Form()
    return { 'object_list' : [], 'form' :form }


