import json , types , sys , csv , tarfile , os

query_file = '../RedditData/reddit_data.json'
movie_ids_file = '../Data/Imdb/movie_ids.txt'
id_to_title_medium_file = '../Data/Imdb/id-to-title-medium.json'
id_to_title_small_file = '../Data/Imdb/id-to-title-small.json'

movie_id_dict = {}
with open(movie_ids_file) as f:
	for line in f:
		line = line.replace('\n','')
		movie_id_dict[line] = []

with open(id_to_title_small_file) as json_file:
	id_title_pairs = json.load(json_file)
	movie_ids = id_title_pairs.keys()

for i in range(len(movie_ids)):
	movie_id_dict[movie_ids[i]].append(id_title_pairs[movie_ids[i]])

with open(id_to_title_medium_file) as json_file:
	id_title_pairs = json.load(json_file)
	movie_ids = id_title_pairs.keys()

for i in range(len(movie_ids)):
	movie_id_dict[movie_ids[i]].append(id_title_pairs[movie_ids[i]])


qrels_list = []

querys = {}

with open(query_file) as json_file:
	reddit_data = json.load(json_file)

question_querys = reddit_data.keys()

for query in question_querys:
	obj = reddit_data[query]
	for item in obj:
		if isinstance(item ,types.UnicodeType ):
			query_id = item
		else:
			suggestion_list = item
	if len(suggestion_list) > 0:
		querys[query_id] = suggestion_list

movie_ids_list = sorted(movie_id_dict.keys())
#print movie_ids_list
counter = 0
for query_id in sorted(querys.keys()):
	suggestion_list = querys[query_id]
	for movie_id in movie_ids_list:
		relevant = False
		for title in movie_id_dict[movie_id]:

			if any(title in s for s in suggestion_list):
				relevant = True
				counter+=1
				break
		
		qrels_list.append([query_id,movie_id,int(relevant)])

with open('qrels.txt','w') as f:
	wr = csv.writer(f,delimiter=' ')
	wr.writerows(qrels_list)
#print len(querys)
#print counter 
#print len(qrels_list)

tar = tarfile.open('qrels.tar.gz','w:gz')
tar.add('qrels.txt')
tar.close()

os.remove('qrels.txt')

