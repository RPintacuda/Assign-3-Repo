import os.path
import requests

from download import download_wikipedia_abstracts
from load import load_documents
from search.timing import timing
from search.index import Index


@timing
def index_documents(documents, index):
    for i, document in enumerate(documents):
        index.index_document(document)
        if i % 5000 == 0:
            print(f'Indexed {i} documents', end='\r')
    return index

def execute_search(index,query,search_type,rank=False):
    print(" ------------------------------------------------------------------------------------------------------- ")
    print("query         = " + query)
    print("search_type   = " + search_type)
    print("Ranked Search = " + str(rank))
    results = index.search(query, search_type,rank)
    print("found "+str(len(results))+ " documents")
    # print(results)
    if rank:
        for doc,score in results:
            print('{0: <10} {1: <10} {2: <60} {3: <50}'.format(score, doc.ID, doc.title, doc.url).encode("utf-8"))
    else:    
        for doc in results:
            print('{0: <10} {1: <60} {2: <50}'.format(doc.ID, doc.title, doc.url).encode("utf-8"))

if __name__ == '__main__':
    # this will only download the xml dump if you don't have a copy already;
    # just delete the file if you want a fresh copy
    if not os.path.exists('data/enwiki-latest-abstract.xml.gz'):
        download_wikipedia_abstracts()

    index = index_documents(load_documents(), Index())
    print(f'Index contains {len(index.documents)} documents')

    execute_search(index, 'London Beer Flood', search_type='AND')
    execute_search(index, 'London Beer Flood', search_type='OR')
    execute_search(index, 'London Beer Flood', search_type='AND', rank=True)
    execute_search(index, 'London Beer Flood', search_type='OR', rank=True)
