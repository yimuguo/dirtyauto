from bs4 import BeautifulSoup
import urllib2

r = urllib2.urlopen('http://www.aflcio.org/Legislation-and-Politics/Legislative-Alerts').read()
soup = BeautifulSoup(r)
print(type(soup))
