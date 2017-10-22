import requests
import re
from bs4 import BeautifulSoup
import sys, os
import time
import json
reload(sys)
sys.setdefaultencoding('utf-8')

key_list = ['Directed by', 'Produced by', 'Written by', 'Screenplay by', 'Starring', 'Music by', 'Cinematography', 'Edited by', 'Production\ncompany', 'Distributed by', 'Release date', 'Running time', 'Country', 'Language', 'Budget', 'Box office']

def find_in_table(table, movie_info):
    th = table.find('th', text='Directed by')
    while th is not None:
        td = th.findNext('td')
        txt = str(td.text).strip('\n')
        key = str(th.text).strip('\n')
        if key in key_list:
            movie_info[key] = txt

        th = th.findNext('th')
    return movie_info

def find_plot(soup):
    plot = ""
    h2 = soup.find('h2')

    while h2 is not None and 'Plot' not in h2.text:
        h2 = h2.findNext('h2')

    if h2 is not None:
        nxt = h2.findNext()
        while nxt is not None and nxt.name != 'h2':
            if nxt.name == 'p':
                plot += str(nxt.text) + '\n'
            nxt = nxt.findNext()
    return plot

def find_response(soup):
    cr = ""
    h2 = soup.find('h2')
    while h2 is not None and 'Critical' not in h2.text and 'Response' not in h2.text:
        h2 = h2.findNext('h2')

    if h2 is not None:
        nxt = h2.findNext()
        while nxt is not None and nxt.name != 'h2':
            if nxt.name == 'p':
                cr += str(nxt.text) + '\n'
            nxt = nxt.findNext()
    return cr


infl = open('movies_title.txt', 'r')
all_movies = {}
i = 0

for line in infl:
    i+=1

    info = line.split(':', 1)
    imdbid = info[0].strip()
    name = info[1].strip()
    print i," Processing ", name
    name = name.replace(' ', '_')

    url = 'https://en.wikipedia.org/wiki/' + name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    movie_info = {'name' : info[1].strip()}
    if soup is not None:
        table = soup.find('table', {'class': 'infobox vevent'})
        if table is not None:
            movie_info = find_in_table(table, movie_info)

        movie_info['plot'] = find_plot(soup)
        movie_info['Critical Response'] = find_response(soup)

    all_movies[imdbid] = movie_info
    time.sleep(.1)


with open("wiki_data.json", "w") as f:
    json.dump(all_movies, f, sort_keys=True, indent=4)
