from bs4 import BeautifulSoup
from os import listdir
import json

directory = "../Data/Imdb/DetailsCrawl"

id_to_details = {}

def find_between(s, first, last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return 

for file in listdir(directory):

	with open(directory + "/" + file) as f:
	
		try:
			soup = BeautifulSoup(f.read(), "lxml")
		except:
			continue

		for link in soup.find_all('link', rel=True, href=True):
			url_look_like = "http://www.imdb.com/title/"
			if url_look_like in link['href']:
				id = find_between(link['href'], url_look_like, "/")

		genres = []
		directors = []
		writers = []
		stars = []
		similar_movies = []
		plot_keywords = []

		for a in soup.find_all('a', href=True):
			if "ref_=tt_ov_inf" in a['href'] and "genre" in a['href']:
				genres.append(a.text)

		for plotsoup in soup.find_all("div", { "class" : "summary_text" }):
			plot = plotsoup.text.strip()

		for div in soup.find_all('div', {"class" : "credit_summary_item"}):
			for tag in div.find_all('span', attrs={"itemprop" : "director"}):
				directors.append(tag.text.strip())
			for tag in div.find_all('span', attrs={"itemprop" : "creator"}):
				writers.append(tag.text.strip())
			for tag in div.find_all('span', attrs={"itemprop" : "actors"}):
				stars.append(tag.text.strip())

		for ratingsoup in soup.find_all('span', {"class" : "rating"}):
			rating = ratingsoup.text.strip()[:-3]

		for tag in soup.find_all('div', {"class" : "rec-title"}):
			for a in tag.find('a'):
				similar_movies.append(a.text.strip())

		for tag in soup.find_all('span', attrs={"itemprop" : "keywords"}):
			plot_keywords.append(tag.text.strip())				

		id_to_details[id] = {
			"genres": genres,
			"plot": plot,
			"directors": directors,
			"writers": writers,
			"stars": stars,
			"rating": rating,
			"similar_movies": similar_movies,
			"plot_keywords": plot_keywords
		}

with open("results.json", "w") as f:
	json.dump(id_to_details, f, sort_keys=True, indent=4)
