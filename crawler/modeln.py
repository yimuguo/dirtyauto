from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


page = requests.get(
    "http://corpqlikprod/QvAJAXZfc/AccessPoint.aspx?open=&id=QVS%40corpqv1%7CSales%2FOpportunityMetrics.qvw&client=Ajax")
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify)
driver = webdriver.Chrome()
driver.get(
    "http://yguo:Bbsit911(!!@corpqlikprod/QvAJAXZfc/opendoc.htm?document=Sales%2FOpportunityMetrics.qvw&host=QVS%40corpqv1")
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_selected('#\31 1 > div.QvCaption > div.QvCaptionImgContainer > div.QvCaptionIcon.caption-icon-16x16.caption-XL-dark-icon'))
send_xls_btn = driver.find_element_by_xpath('//*[@id="11"]/div[1]/div[1]/div[1]')
print(send_xls_btn)
send_xls_btn.click()
