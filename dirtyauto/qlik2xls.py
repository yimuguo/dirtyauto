from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import configparser
import time
import win32com.client


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


class ProcessCFG(object):
    """
    Process settings .ini configurations
    """

    intranet = 'yes'
    usr = None
    pwd = None
    profile = 'DEFAULT'
    download_dir = None

    def __init__(self, file):
        self.file = file
        self._config = configparser.ConfigParser()
        # self._config.read('qlik2xls.ini')
        self._config.read(file)
        self.pre_process()
        self.process_cfg()

    def pre_process(self):
        if self._config['DEFAULT']:
            if self._config['DEFAULT']['active_profile']:
                self.profile = self._config['DEFAULT']['active_profile']
                if not self._config[self.profile]['intranet']:
                    raise ValueError('\"intranet\" option not found in active profile')
                if self._config[self.profile]['intranet'] != 'yes':
                    if self._config[self.profile]['usr']:
                        if self._config[self.profile]['pwd']:
                            pass
                        else:
                            raise ValueError('No password in config file while outside of intranet')
                    else:
                        raise ValueError('No username in config file while outside of intranet')
            else:
                self.profile = 'DEFAULT'
                if not self._config[self.profile]['intranet']:
                    raise ValueError('\"intranet\" option not found in active profile')
        else:
            print(self.file + " DEFAULT PROFILE NOT VALID IN DIRECTORY, CREATING DEFAULT CONFIG FILE")
            self._config['DEFAULT'] = {'intranet': 'yes',
                                       'download_dir': 'os_default',
                                       'active_profile': 'DEFAULT'}
            with open(self.file, 'w+') as file:
                self._config.write(file)
            self.profile = 'DEFAULT'

    def process_cfg(self):
        self.intranet = self._config[self.profile]['intranet']
        self.dowload_dir = self._config[self.profile]['download_dir']
        if self.profile != 'DEFAULT' and self.intranet != 'yes':
            self.usr = self._config[self.profile]['usr']
            self.pwd = self._config[self.profile]['pwd']


def main():
    # Read/Create _configuration File Contains Username/Password Info
    config = ProcessCFG('./qlik2xls.ini')

    print("Current profile " + config.profile + '\n')

    driver = webdriver.Chrome()
    driver.get(
        "http://corpqlikprod/QvAJAXZfc/opendoc.htm?document=Sales%2FOpportunityMetrics.qvw&host=QVS%40corpqv1")
    driver.maximize_window()

    if config.intranet != 'yes':
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.Sendkeys(config.usr)
        shell.Sendkeys("{TAB}")
        shell.Sendkeys(config.pwd)
        shell.Sendkeys("{ENTER}")

    import pdb; pdb.set_trace()  # breakpoint 2ed8fdbc //
    all_opp = click_by_text('All Opportunities', driver, timeout=100)

    # funnel_filter_switch = click_by_xpath(
    #     '//*[@id="75"]/div[3]/div/div[1]/div[5]/div/div[3]/div[1]', driver, timeout=60)
    # funnel_filter_switch = click_by_xpath(
    #     '//*[@id="74"]/div[3]/div/div[1]/div[5]/div/div[3]', driver, timeout=60)
    # time.sleep(3)
    ref_des_switch = click_by_xpath(
        '//*[@title="No"]//*[@unselectable="on"]', driver, timeout=120)

    funnel_filter_switch = click_by_xpath(
        '//*[@title="Pending"]//*[@unselectable="on"]', driver, timeout=120)

    # send2xls = click_by_xpath('//*[@id="79"]/div[1]/div[1]/div[1]', driver, timeout=100)
    send2xls = click_by_title('Send to Excel', driver, timeout=120)


if __name__ == '__main__':
    main()
