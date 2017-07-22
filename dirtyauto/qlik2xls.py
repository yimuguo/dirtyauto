from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import configparser
import time
import win32com.client


def make_cfg():
    _config = configparser.ConfigParser()
    _config['DEFAULT'] = {'Intranet': 'yes',
                          'dowload_dir': '%%USERPROFILE%%/Downloads'}
    with open('qlik2xls.ini', 'w+') as file:
        _config.write(file)
    return _config


def click_by_text(txt, _driver, timeout=30):
    wait = WebDriverWait(_driver, timeout)
    wait.until(expected_conditions.element_to_be_clickable(
        (By.XPATH, "//*[contains(text(), '%s')]" % txt)))
    element = _driver.find_element_by_xpath(
        "//*[contains(text(), '%s')]" % txt)
    element.click()
    return element


def click_by_xpath(xpath, _driver, timeout=30):
    wait = WebDriverWait(_driver, timeout)
    wait.until(expected_conditions.element_to_be_clickable(
        (By.XPATH, xpath)))
    element = _driver.find_element_by_xpath(xpath)
    time.sleep(5)
    element.click()
    return element


def click_by_title(title, _driver, timeout=30):
    wait = WebDriverWait(_driver, timeout)
    wait.until(expected_conditions.element_to_be_clickable(
        (By.XPATH, '//*[@title="%s"]' % title)))
    element = _driver.find_element_by_xpath(
        '//*[@title="%s"]' % title)
    element.click()
    return element


def main():
    # Read/Create Configuration File Contains Username/Password Info
    config = configparser.ConfigParser()
    config.read('qlik2xls.ini')

    if config['DEFAULT']:
        if config['DEFAULT']['active_profile']:
            USER_PROFILE = config['DEFAULT']['active_profile']
            if not config[USER_PROFILE]['Intranet']:
                raise ValueError('\"Intranet\" option not found in active profile')
        else:
            USER_PROFILE = 'DEFAULT'
            if not config[USER_PROFILE]['Intranet']:
                raise ValueError['\"Intranet\" option not found in active profile']
    else:
        raise Exception("qlik2xls.ini DEFAULT PROFILE NOT VALID IN DIRECTORY, CREATING DEFAULT CONFIG FILE")
        config = make_cfg()

    print("Current profile " + USER_PROFILE + '\n')
    usr_flg = config[USER_PROFILE]['Intranet']

    driver = webdriver.Chrome()
    driver.get(
        "http://corpqlikprod/QvAJAXZfc/opendoc.htm?document=Sales%2FOpportunityMetrics.qvw&host=QVS%40corpqv1")
    driver.maximize_window()

    if usr_flg != 'yes':
        shell = win32com.client.Dispatch("WScript.Shell")
        usr = config[USER_PROFILE]['usr']
        pwd = config[USER_PROFILE]['pwd']
        shell.Sendkeys(usr)
        shell.Sendkeys("{TAB}")
        shell.Sendkeys(pwd)
        shell.Sendkeys("{ENTER}")

    all_opp = click_by_text('All Opportunities', driver, time)

    # funnel_filter_switch = click_by_xpath(
    #     '//*[@id="75"]/div[3]/div/div[1]/div[5]/div/div[3]/div[1]', driver, timeout=60)
    # funnel_filter_switch = click_by_xpath(
    #     '//*[@id="74"]/div[3]/div/div[1]/div[5]/div/div[3]', driver, timeout=60)
    # time.sleep(3)
    funnel_filter_switch = click_by_xpath('//*[@title="Pending"]//*[@unselectable="on"]', driver, timeout=100)

    # send2xls = click_by_xpath('//*[@id="79"]/div[1]/div[1]/div[1]', driver, timeout=100)
    import pdb; pdb.set_trace()  # breakpoint fe22be2e //
    send2xls = click_by_title('Send to Excel', driver, timeout=100)

    driver.get("chrome://downloads")
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.Sendkeys("Full Opp Funnel")


if __name__ == '__main__':
    main()
