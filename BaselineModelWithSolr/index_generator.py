import json

print "Readin from json file...."
with open('id-to-reviews.json') as json_data:
    dic = json.load(json_data)

print "Creating index...."

index = []

for key in dic:
    dk = {}
    txt = ""
    for review in dic[key]:
        txt += review['text']
    if len(txt)>30000:
        txt = txt[0:30000]
    #print key
    dk["imdb_id"] = key
    dk["reviews"] = txt
    index.append(dk)

print "Writing to json file...."
with open("imdb_review_index.json", "w") as f:
        json.dump(index, f, sort_keys=True, indent=4)

print "Total files: ", len(index)

### Drive link for indexed file :
##   https://drive.google.com/file/d/0B9o5ykSODCIlbWlVbDNuR21JejQ/view?usp=sharing


#### use command :
# $ curl http://localhost:8983/solr/ire/update -H 'Content-type:application/json' -d @imdb_review_index.json
# to add data to solr database
