from urllib2 import *
import urllib
import re


while True:

    query = raw_input('Search Movie > ')

    if query == 'quit' or query == 'exit':
        break

    query = re.split(r'[^A-Za-z]+', query)

    solr_query = ''
    i=0
    for word in query:
        i+=1
        solr_query += 'reviews:"' + word + '"'
        if i != len(query):
            solr_query += ' OR '

    qouted_solr_query = urllib.quote(solr_query)
    solr_url = 'http://localhost:8983/solr/ire/select?q=%s&wt=python' % (qouted_solr_query)
    print solr_url
    print

    connection = urlopen(solr_url)
    response = eval(connection.read())

    i=0
    for doc in response['response']['docs']:
        i+=1
        print i, doc['imdb_id']
