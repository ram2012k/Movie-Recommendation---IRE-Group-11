import praw, urllib3, bs4, os, re, json, io, time, selenium
from praw.models import MoreComments

#https://www.reddit.com/r/MovieSuggestions/top.json?limit=10000
def main():
  proxy = urllib3.ProxyManager('http://proxy.iiit.ac.in:8080/')
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

  divs = []
  titles = []
  stop = 0
  addresses = []
  
  with open('addresses.txt') as f:
    lines = f.readlines()
    for line in lines:
      addresses.append(line)

  for address in addresses:
    stop = stop + 1
    addr = address.strip()
    r = proxy.request('GET', addr)
    print (addr)
    soup = bs4.BeautifulSoup(r.data, "html.parser")
    allDivs = soup.findAll("div", id = re.compile("thing_t3_"))
    
    for div in allDivs:
      td = div.get('class', [])
      print (td[2][6:])
      divs.append(td[2][6:])

    allTitles = soup.findAll("a", class_ = re.compile("title"))
    for title in allTitles:
      titles.append(title.contents[0])
    print (stop, 'out of', len(addresses))
    if stop%10==0:
      time.sleep(30)

  comments = []
  stop = 0
  for ids in divs:
    stop = stop + 1
    reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',client_id='iEBaMKbr5HFLzA', client_secret="y6MxWDxI64H8l02OCCi_z5sNMtw")
    address = 'http://www.reddit.com/r/MovieSuggestions/comments/' + ids + '/'
    submission = reddit.submission(url = address)
    temp = []
    for top_level_comment in submission.comments:
      if isinstance(top_level_comment, MoreComments):
        continue
      temp.append(top_level_comment.body)
    comments.append(temp)

    print (stop, 'out of', len(divs))
    if stop%100==0:
      time.sleep(30)

  data = {}
  for i in range(len(divs)):
    temp = []
    address = 'http://www.reddit.com/r/MovieSuggestions/comments/' + ids + '/'
    temp.append(divs[i])
    temp.append(comments[i])
    data[titles[i]] = temp
    print (i, titles[i], divs[i])
  print (len(data))
  with open('reddit_data2.json', 'w') as f:
    json.dump(data, f, ensure_ascii = False)

if __name__ == "__main__":
  main()
