
import os
import sys
import requests
import urlparse
from BeautifulSoup import BeautifulSoup

props_list = [
  "givenName",
  "familyName",
  "jobTitle",
  "email",
  "telephone",
  "workLocation"
]

pub_class_list = [
  "publicationTitle",
  "publicationAuthors",
  "publicationDetails"
]

class PeopleGroup:
  def __init__(self, base_url):
    self.base_url = base_url
    parse_url_obj = urlparse.urlsplit(self.base_url)
    self.root_url = "%s://%s" % (parse_url_obj.scheme, parse_url_obj.netloc)
    print self.root_url

  def generate(self):
    r = requests.get(self.base_url)
    soup = BeautifulSoup(r.text)

    indices = soup.findAll('p', attrs={"class": "personIndex"})
    print "We have found %d people:" % len(indices)
    for index in indices:
      a = index.find('a', href=True)
      print "\nFetching %s's profile from %s ..." % (a.text, a['href'])
      r = requests.get("%s%s" % (self.root_url, a['href']))
      soup = BeautifulSoup(r.text)
      content = soup.find('div', id="content")
      
      for prop in props_list:
        print "%s:\t" % prop,
        result = []
        for s in soup.findAll(attrs={"itemprop": prop}):
          t = ' '.join(s.text.strip().split())
          result.append(t)
        print result

      print "Publications:"
      pub_result = []
      for pub in soup.findAll('td', attrs={"class":"publicationInfo"}):
        pub_dict = {}
        for pub_class in pub_class_list:
          s = pub.find(attrs={"class":pub_class})
          if s:
            pub_dict[pub_class] = ' '.join(s.text.strip().split())
        pub_result.append(pub_dict)
      for idx, result in enumerate(pub_result):
        print "%3d:\t%s" % (idx, result["publicationTitle"])

base_url_list = [
  "http://www.cs.ox.ac.uk/people/peopleA.html"
]

if __name__ == '__main__':

  for base_url in base_url_list:
    print "Select base url %s ..." % base_url
    people_group = PeopleGroup(base_url)
    print "Generating group ..."
    people_group.generate()
