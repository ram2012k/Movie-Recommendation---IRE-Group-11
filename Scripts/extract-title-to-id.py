from bs4 import BeautifulSoup
from os import listdir
import json

directory = "../Data/Imdb/Titles"

id_to_movie = {}

for file in listdir(directory):
	with open(directory + "/" + file) as f:
		soup = BeautifulSoup(f.read(), "lxml")
		for a in soup.find_all('a', href=True):
			if "ref_=adv_li_tt" in a['href']:
				id = a['href'][7:-16]
				if id not in id_to_movie:
					id_to_movie[id] = a.text

with open("results.json", "w") as f:
	json.dump(id_to_movie, f, sort_keys=True, indent=4)


				

