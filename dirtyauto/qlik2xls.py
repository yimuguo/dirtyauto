from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import win32com.client


def click_by_text(txt, _driver, timeout=10):
    wait = WebDriverWait(_driver, timeout)
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[contains(text(), '%s')]" % txt)))
    element = _driver.find_element_by_xpath("//*[contains(text(), '%s')]" % txt)
    element.click()
    return element


def click_by_xpath(xpath, _driver, timeout=10):
    wait = WebDriverWait(_driver, timeout)
    wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpath)))
    element = _driver.find_element_by_xpath(xpath)
    element.click()
    return element


driver = webdriver.Chrome()
driver.get("http://corpqlikprod/QvAJAXZfc/opendoc.htm?document=Sales%2FOpportunityMetrics.qvw&host=QVS%40corpqv1")
driver.maximize_window()
shell = win32com.client.Dispatch("WScript.Shell")
shell.Sendkeys("yguo")
shell.Sendkeys("{TAB}")
shell.Sendkeys("Bbsit911{(}!!")
shell.Sendkeys("{ENTER}")

all_opp = click_by_text('All Opportunities', driver)
# all_opp = find_by_text('All Opportunities', driver)

funnel_filter_switch = click_by_xpath('//*[@id="75"]/div[3]/div/div[1]/div[5]/div/div[3]/div[1]', driver)

send2xls = click_by_xpath('//*[@id="60"]/div[1]/div[1]/div[1]', driver)
