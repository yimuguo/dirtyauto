from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import sys
import configparser


try:
    USER_PROFILE = sys.argv[1]
except IndexError:
    print("No argument pass as default profile")
    USER_PROFILE = "DEFAULT"


def make_cfg():
    _config = configparser.ConfigParser()
    _config['DEFAULT'] = {'Intranet': 'yes',
                          'dowload_dir': '%USERPROFILE%/Downloads'}
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
    wait.until(expected_conditions.visibility_of_element_located(
        (By.XPATH, "//*[contains(text(), '%s')]" % txt)))
    element = _driver.find_element_by_xpath(
        "//*[contains(text(), '%s')]" % txt)
    element.click()
    return element


def click_by_xpath(xpath, _driver, timeout=30):
    wait = WebDriverWait(_driver, timeout)
    wait.until(expected_conditions.visibility_of_element_located(
        (By.XPATH, xpath)))
    element = _driver.find_element_by_xpath(xpath)
    element.click()
    return element


def main():
    # Read/Create Configuration File Contains Username/Password Info
    config = configparser.ConfigParser()
    config.read('qlik2xls.ini')
    if config.sections():
        if USER_PROFILE is not 'DEFAULT':
            if config[USER_PROFILE]:
                if config[USER_PROFILE]['usr']:
                    if config[USER_PROFILE]['pwd']:
                        pass
                    else:
                        sys.exit("\"pwd\" IS NOT PRESENT IN CONFIG FILE\n")
                else:
                    sys.exit("\"usr\" IS NOT PRESENT IN THE CONFIG FILE\n")
            else:
                sys.exit("USERPROFILE NOT FOUND IN CONFIG FILE\n")
    else:
        print("qlik2xls NOT FOUND IN DIRECTORY, CREATING DEFAULT CONFIG FILE")
        config = make_cfg()
    usr_flg = config[USER_PROFILE]['Intranet']

    driver = webdriver.Chrome()
    driver.get(
        "http://corpqlikprod/QvAJAXZfc/opendoc.htm?document=Sales%2FOpportunityMetrics.qvw&host=QVS%40corpqv1")
    driver.maximize_window()
    if usr_flg is not 'yes':
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        usr = config[USER_PROFILE]['usr']
        pwd = config[USER_PROFILE]['pwd']
        shell.Sendkeys(usr)
        shell.Sendkeys("{TAB}")
        shell.Sendkeys(pwd)
        shell.Sendkeys("{ENTER}")

    all_opp = click_by_text('All Opportunities', driver)

    funnel_filter_switch = click_by_xpath(
        '//*[@id="75"]/div[3]/div/div[1]/div[5]/div/div[3]/div[1]', driver)

    send2xls = click_by_xpath('//*[@id="60"]/div[1]/div[1]/div[1]', driver)


if __name__ == '__main__':
    main()
