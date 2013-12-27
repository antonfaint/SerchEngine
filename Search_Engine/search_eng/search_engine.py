# -*- coding: utf-8 -*-
#from  nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
#import pymorphy
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup, SoupStrainer
from Queue import Queue
from time import time
import re

wordPattern_en = re.compile("((?:[a-zA-Z]+[-']?)*[a-zA-Z]+)")


MAX_DEPTH = 3

class Link_index:
    def __init__( self, url, w, pos_list ):
        self.url = url
        self.weight = w
        self.pos_list = pos_list

    def weight_up(self):
        self.weight = self.weight + 1

    def update(self, pos):
        self.weight_up()
        self.pos_list.append( pos )

    def __eq__(self, other):
        return self.url == other

    def __lt__(self, other):
        return self.weight < other.weight

    def __gt__(self, other):
        return self.weight > other.weight

def Normalize_en(word ):
    n_word = wordnet.morphy( word )
    if n_word:
        return n_word
    else:
        return ""


class IndexGenerator:
    def __init__(self):
        self.index_dict = {}
        self.current_url = ""


    def gen_url_index(self, url, text):
        self.current_url = url
        self.start_gen( text, wordPattern_en, Normalize_en )

    def start_gen( self, text, wordPattern, Normalize):
        pos = 0
        current_index_dict = {}
        for word in wordPattern.findall( text ):
            word = word.strip()
            n_word = Normalize(  word )
            if n_word != "":
                if n_word not in current_index_dict:
                    current_index_dict[n_word] = Link_index( self.current_url, 1, [ pos ] )
                else:
                    current_index_dict[n_word].update( pos )
            pos = pos + 1
        for key in current_index_dict:
            self.add_word_to_index( key, current_index_dict[key] )

    def add_word_to_index( self, word,  index_info ):
        if word in self.index_dict:
            self.index_dict[word].append( index_info )
        else:
            self.index_dict[ word ] = [ index_info ]


    def get_index_dict(self):
        return self.index_dict



def get_page(url):
	try:
		f = urlopen(url)
		page = f.read()
		f.close()
		return page
	except:
		return ""
	return ""


def link_generator( html ):
    for link in BeautifulSoup( html, parseOnlyThese=SoupStrainer('a') ):
        if link.has_key( 'href' ):
            if str( link[ 'href' ] ).startswith( 'http' ):
                yield link[ 'href' ]



def Create_index_from_url( url, depth ):
    url_index = {}
    word_index_dict = {}
    if depth > MAX_DEPTH:
        return []
    url_queue = Queue()
    url_queue.put( url )
    checked = []
    page_index_list = []

    IndexGen = IndexGenerator()
    while not url_queue.empty() :

        current_url = url_queue.get()

        checked.append( current_url )

        try:
            html = get_page( current_url )
        except:
            print "Exception"
            continue
        if depth > 0:
            for link in link_generator( html ):
                #print link
                if link not in checked:
                    url_queue.put( link )
            depth = depth - 1

        html = nltk.clean_html( html )
        IndexGen.gen_url_index( current_url, html )

        Result = IndexGen.get_index_dict()
        for key in Result:
            Result[key].sort()


    return Result


class Query_info:
    def __init__(self, url,  w):
        self.url = url
        self.num_word = 1
        self.sum_weight = w

    def update(self, w):
        self.num_word = self.num_word + 1
        self.sum_weight = self.sum_weight + w

    def __lt__(self, other):
        if self.num_word == other.num_word:
            return self.sum_weight < other.sum_weight
        else:
            return self.num_word < self.sum_weight




def query_weight( query_list_word, index ):

    url_dict = {}
    for word in query_list_word:
        if word in index:
            print word
            for url_info in index[word]:
                if url_info.url in url_dict:
                    url_dict[ url_info.url ].update( url_info.weight )
                else:
                    url_dict[ url_info.url ] = Query_info( url_info.url, url_info.weight )
    Result = []
    for key in url_dict:
        Result.append( url_dict[ key ] )
    Result.sort()
    return Result




def Query_run( text_query, index ):
    query_norm_list = []
    for word in wordPattern_en.findall( text_query ):
        word = word.strip()
        n_word = Normalize_en(  word )
        if n_word != "":
            query_norm_list.append( n_word )

    print query_norm_list
    return query_weight( query_norm_list, index )


# Может быть протестированно без джанго, как отдельный модуль
def Test():
    t = time()
    Index = Create_index_from_url( "http://stackoverflow.com/questions/17669952/finding-proper-nouns-using-nltk-wordnet", 0 )
    print time() - t

    for keyword in Index:

        print "##################"
        print keyword
        for url_info in Index[ keyword ]:
            print str(  url_info.url ) + "  " + str(  url_info.weight ) + "  " +str(  url_info.pos_list )
        print "*****************"
    print time() - t
def TestQuery():
    t = time()
    Index = Create_index_from_url( "http://stackoverflow.com/questions/17669952/finding-proper-nouns-using-nltk-wordnet", 1 )
    for res in Query_run( "nltk wordnet order",Index ):
        print res.url
    print time() - t

#TESTS
#Test()
#TestQuery()