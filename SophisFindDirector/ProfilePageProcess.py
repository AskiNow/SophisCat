
# This is a single profile page processor:
# [input]   HTML file of the profile page, and this page could be quite irregular
# [output]  a profile dictionary of user.

import os
import sys
import requests
from BeautifulSoup import BeautifulSoup

attrs = [
  "itemprop",
  "class"
]

basic_props = [
  "givenName",
  "familyName",
  "jobTitle",
  "email",
  "telephone",
  "workLocation"
]
pub_props = [
  "publicationTitle",
  "publicationAuthors",
  "publicationDetails"
]

prop_groups = {
  "publication": ("publicationInfo", pub_props)
}

class ProfilePage:
  def __init__(self, source):
    self.soup = BeautifulSoup(source)
    self.result = {}

  def run(self):
    print "Parsing basic properties ..."
    for prop in basic_props:
      self.result[prop] = []
      for attr in attrs:
        for s in self.soup.findAll(attrs={attr: prop}):
          self.result[prop].append(s.text)

    print "Parsing property groups ..."
    for group_name, prop_group in prop_groups.items():
      print "Parsing %s group ..." % name
      self.result[group_name] = []
      for attr in attrs:
        for sg = soup.findAll(attrs={attr:prop_group[0]}):
          for prop in prop_group[1]:
            for s = sg.findAll(attrs)


    pass

if __name__ == '__main__':
  if len(sys.argv) <= 1:
    print "usage: %s <profile-url>" % sys.argv[0]
    exit(1)

  url = sys.argv[1]

  print "*** Profile page processor example program ***"
  print "Ready to parse page from url %s ..." % url
  r = requests.get(url)
  if r.status_code != 200:
    print "Something wrong while fetching page: %d" % r.status_code
    exit(1)
  print "Successfully fetched page: %d" % r.status_code

  profile_page = ProfilePage(r.text)
  profile_page.run()