from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import sys
import configparser
import time
import win32com.client


try:
    USER_PROFILE = sys.argv[1]
except IndexError:
    print("No argument pass as default profile")
    USER_PROFILE = "DEFAULT"


def make_cfg():
    _config = configparser.ConfigParser()
    _config['DEFAULT'] = {'Intranet': 'yes',
                          'dowload_dir': '%%USERPROFILE%%/Downloads'}
    if USER_PROFILE is not 'DEFAULT':
        _config[USER_PROFILE]['Intranet'] = 'no'
        usr = input("Input your username:\n")
        pwd = input("Password:\n")
        _config[USER_PROFILE]['usr'] = usr
        _config[USER_PROFILE]['pwd'] = pwd
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
    if config[USER_PROFILE]:
        if not config[USER_PROFILE]['Intranet']:
            raise ValueError('\"Intranet\" option not found in configuration')
        if USER_PROFILE != 'DEFAULT':
            if config[USER_PROFILE]:
                if config[USER_PROFILE]['usr']:
                    if config[USER_PROFILE]['pwd']:
                        pass
                    else:
                        raise ValueError("\"pwd\" IS NOT PRESENT IN CONFIG FILE\n")
                else:
                    raise ValueError("\"usr\" IS NOT PRESENT IN THE CONFIG FILE\n")
            else:
                raise ValueError("USERPROFILE NOT FOUND IN CONFIG FILE\n")
    else:
        print("qlik2xls NOT FOUND IN DIRECTORY, CREATING DEFAULT CONFIG FILE")
        config = make_cfg()
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

    all_opp = click_by_text('All Opportunities', driver)

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
