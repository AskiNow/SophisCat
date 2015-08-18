

import os
import sys
import requests
from bs4 import BeautifulSoup
import html
from time import sleep

dblp_person_base_url = "http://dblp.uni-trier.de/pers/hd/t/"

persons = {}

class Connection:
  def __init__(self, url, articles=[]):
    self.url = url
    self.articles = articles

class Article:
  def __init__(self, title, conf, date):
    self.title = title
    self.conf = conf
    self.date = date

  def __repr__(self):
    return "%s <%s %s>" % (self.title, self.conf, self.date)

class Person:
  def __init__(self, name, url, alias=[]):
    self.name = name
    self.url = url
    self.alias = alias
    self.conns = {}
    pass

  def __repr__(self):
    return "%s" % (self.name)

  def parse(self):
    print("Parsing %s ..." % self.name)
    r = requests.get(self.url)
    if r.status_code != 200:
      print("Something wrong: %d" % r.status_code)
      exit(1)
    soup = BeautifulSoup(r.text, "html.parser")
    urls = {}
    # parse each publication
    for pub in soup.findAll('div', attrs={'class':'data'}):
      # parse to get article information
      title = pub.find('span', {'class':'title', 'itemprop': 'name'})
      conf =  pub.find('span', {'itemprop': 'isPartOf'})
      date =  pub.find('span', {'itemprop': 'datePublished'})
      if title != None: title = title.text
      if conf  != None: conf  = conf.text
      if date  != None: date  = date.text
      article = Article(title, conf, date)

      # parse to get authors
      for author in pub.findAll(attrs={'itemprop': 'author'}):
        name = html.unescape(author.text)
        a = author.find('a', href=True)
        if a: # Contains url link
          url = a['href']
          if url in urls:
            urls[url].add(name)
          else:
            urls[url] = set([name])
      
      # add connections
      for url, names in urls.items():
        # first find out whether this url exists in the hash list
        names = list(names)
        if url not in persons:
          persons[url] = Person(names[0], url, names[1:])
        if url in self.conns:
          self.conns[url].articles.append(article)
        else:
          self.conns[url] = Connection(url, [article])

class UrlPool:
  def __init__(self):
    self.urls = {}
    self.count = 0

  def empty(self):
    return self.count == 0

  def push(self, url):
    if url not in self.urls:
      self.urls[url] = 0
      self.count += 1

  def pop(self):
    if self.count == 0:
      return None
    for url in self.urls:
      if self.urls[url] == 0:
        self.urls[url] = 1
        self.count -= 1
        return url


if __name__ == '__main__':
  urlpool = UrlPool()
  p = Person("Tim Todman", "http://dblp.uni-trier.de/pers/hd/t/Todman:Tim")
  f = open('datefile.txt', 'w')
  while True:
    sleep(3)
    p.parse()
    print("%s has %d connections:" % (p.name, len(p.conns)))
    for i, conn in enumerate(p.conns):
      print("%3d: %3d articles\t %s " % 
        (i,  len(p.conns[conn].articles), persons[conn]))
      urlpool.push(conn)
    print("UrlPool has %d number of people to search" % urlpool.count)
    if urlpool.empty():
      break
    p = persons[urlpool.pop()]

    for conn in p.conns:
      print >>f, "%s, %s"
    