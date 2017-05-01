from bs4 import BeautifulSoup
import requests

page = requests.get("http://direct.modeln.idt.com/")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify)
