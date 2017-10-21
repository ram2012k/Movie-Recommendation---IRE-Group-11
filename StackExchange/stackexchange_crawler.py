import praw, urllib3, bs4, os, re, json, io, time
from praw.models import MoreComments

def main():
  proxy = urllib3.ProxyManager('http://proxy.iiit.ac.in:8080/')
  urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
  urlPart1 = 'https://movies.stackexchange.com/questions/tagged/identify-this-movie?page=' 
  urlPart2 = '&sort=newest&pagesize=15'
  
  data = {}
  addresses = []
  stop = 0
  for i in range(1, 260):
    stop = stop + 1
    url = urlPart1 + str(i) + urlPart2
    r = proxy.request('GET', url)
    print (i, 'out of', 259)
    soup = bs4.BeautifulSoup(r.data, 'html.parser')
    allDivs = soup.findAll('div', class_ = re.compile('question-summary'))
    
    for div in allDivs:
      addr = ''
      valid = 1
      for a in div.find_all('a', href = True):
        addr = a['href']
        break
      subdiv = div.find_all('div', class_ = re.compile('\\bstats\\b'))
      for s in subdiv:
        temp = s.find('span').contents[0]
        temp2 = int(temp.contents[0])
        if temp2 < 0:
          valid = 0
      subdiv = div.find_all('div', class_ = re.compile('status unanswered'))
      if subdiv:
        valid = 0
      if valid == 1:
        addresses.append(addr)

    if stop%30==0:
      time.sleep(30)

  stop = 0
  for address in addresses:
    stop = stop + 1
    print (stop, 'out of', len(addresses))
    addr = 'https://movies.stackexchange.com' + address
    r = proxy.request('GET', addr)
    soup = bs4.BeautifulSoup(r.data, 'html.parser')
    
    #for title of question
    titleDiv = soup.findAll('h1', itemprop = re.compile('name'))
    title = ''
    for div in titleDiv:
      for a in div.find_all('a'):
        title = a.contents[0]

    #for description of question
    descriptionDiv = soup.findAll('td', class_ = re.compile('postcell'))
    content = ''
    for div in descriptionDiv:
      for p in div.find_all('p'):
        if len(p.contents) == 0:
          continue
        if isinstance(p.contents[0], bs4.element.NavigableString):
          content = content + p.contents[0]

    #for answers
    answersDiv = soup.findAll('td', class_ = re.compile('answercell'))
    answers = []
    for div in answersDiv:
      answer = ''
      for p in div.find_all('p'):
        if len(p.contents) == 0:
          continue
        if isinstance(p.contents[0], bs4.element.NavigableString):
          answer = answer + p.contents[0]
      answers.append(answer)

    #for votes corresponding to each answer
    votes = []
    votesDiv = soup.findAll('span', class_ = re.compile('vote-count-post'))
    first = 1
    for div in votesDiv:
      if first == 1:
        first = 0
        continue
      votes.append(div.contents[0])
    
    temp = []
    temp.append(addr)
    temp.append(content)
    temp2 = []
    for i in range(len(answers)):
      temp3 = []
      temp3.append(votes[i])
      temp3.append(answers[i])
      temp2.append(temp3)
    temp.append(temp2)
    data[title] = temp

    if stop%60==0:
      time.sleep(30)

    with open('stackexchange_data.json', 'w') as f:
      json.dump(data, f, ensure_ascii = False)

if __name__ == "__main__":
  main()
