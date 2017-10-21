import os

url = "http://www.imdb.com/title/<id>/reviews?start=<reviewnumber>"

page_limit = 5

with open('../Data/Imdb/movie_ids.txt', 'r') as f:
    ids = [line.strip() for line in f.readlines()]

for id in ids:
	for page in range(page_limit):
		cur_url = url.replace("<id>", id).replace("<reviewnumber>", str(page*10))
		os.system("wget '" + cur_url + "'")