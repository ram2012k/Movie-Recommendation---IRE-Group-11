import json
import wikipedia
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')
import time

fnd = open('found.json', 'w+')
nf = open('notfound.json', 'w+')

with open('movies.json') as json_data:
    dic = json.load(json_data)

i=0
for key in dic:
    i+=1
    print i," Finding ", dic[key]
    res = None
    ans = None
    try:
        t = wikipedia.page(dic[key])
    except wikipedia.exceptions.DisambiguationError as e:
        res = str(e)
    except wikipedia.exceptions.PageError as e1:
        res = None

    if res is not None:
        res = res.split('\n')
        for line in res:
            if "film" in line:
                ans = line
                break
    elif t is None:
        ans = None
    else:
        ans = str(t.title)

    if ans is None:
        nf.write(key + ' : ' + dic[key] + '\n')
    else:
        fnd.write(key + ' : ' + ans + '\n')
    time.sleep(.15)
