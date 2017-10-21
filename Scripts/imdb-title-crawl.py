import os

url = "http://www.imdb.com/search/title?genres=<genre>&view=simple&sort=num_votes,desc&page=<pagenumber>"

# Get genres from file
with open('genres.txt') as f:
    genres = [line.strip().lower() for line in f.read().splitlines()]

# 50 entries per page. Already crawled pages 1, 2
start_from_pageno = 3
end_at_pageno = 5

for genre in genres:
	for page in range(start_from_pageno, end_at_pageno + 1):
		cur_url = url.replace("<genre>", genre).replace("<pagenumber>", str(page))
		os.system("wget '" + cur_url + "'")