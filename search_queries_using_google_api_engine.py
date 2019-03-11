import os
import argparse
from google.appengine.api import search

parser = argparser.ArgumentParser()
parser.add_argument('-n','--first-last', help = "First Name and Last Name")
parser.add_argument('-l','--location', help = "Location")
parser.add_argument('-o','--organisation',help = "Organisation")
args = parser.parse_args()

def query_offset(index, query_string):
    offset = 0
    query_string = 'Name:'+args.first-last+' AND Location:'+args.location+'AND Organisation:'+args.organisation
    while True:
        # Build the query using the current offset.
        options = search.QueryOptions(offset=offset)
        query = search.Query(query_string=query_string, options=options)

        # Get the results
        results = index.search(query)

        number_retrieved = len(results.results)
        if number_retrieved == 0:
            break

        offset += number_retrieved

        documents+= [document for document in results]
    return documents
