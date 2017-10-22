from bs4 import BeautifulSoup
from os import listdir
import json

directories = [
	"../Data/Imdb/ReviewsCrawl1",
	"../Data/Imdb/ReviewsCrawl2"
	]

id_to_reviews = {}

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return 

for directory in directories:
	for file in listdir(directory):
		with open(directory + "/" + file) as f:

			try:
				soup = BeautifulSoup(f.read(), "lxml")
			except:
				continue

			for link in soup.find_all('link', rel=True, href=True):
				url_look_like = "http://www.imdb.com/title/"
				if url_look_like in link['href']:
					id = find_between(link['href'], url_look_like, "/reviews")

			reviews = []

			for h2 in soup.find_all('h2'):
				review = {}
				review["title"] = h2.text
				review["text"] = h2.parent.find_next_sibling('p').text
				reviews.append(review)
			
			if id in id_to_reviews:
				id_to_reviews[id] += reviews
			else:
				id_to_reviews[id] = reviews

with open("results.json", "w") as f:
	json.dump(id_to_reviews, f, sort_keys=True, indent=4)


				

