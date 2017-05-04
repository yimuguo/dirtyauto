from bs4 import BeautifulSoup
import requests

page = requests.get("http://corpqlikprod/QvAJAXZfc/AccessPoint.aspx?open=&id=QVS%40corpqv1%7CSales%2FOpportunityMetrics.qvw&client=Ajax")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify)
