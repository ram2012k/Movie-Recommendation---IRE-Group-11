import os

url = "http://www.imdb.com/title/<id>/"

with open('../Data/Imdb/movie_ids.txt', 'r') as f:
    ids = [line.strip() for line in f.readlines()]

for id in ids:
	cur_url = url.replace("<id>", id)
	os.system("wget '" + cur_url + "'")