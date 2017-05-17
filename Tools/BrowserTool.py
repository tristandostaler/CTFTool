#!/usr/bin/env python
# pip install selenium
# pip install ipython
# pip install jsbeautifier
# pip install requests
# also install https://github.com/mozilla/geckodriver/releases
# sudo mv geckodriver /usr/bin
# export PATH=$PATH:/usr/bin/geckodriver
# then run script
# https://websec.wordpress.com/2010/12/04/sqli-filter-evasion-cheat-sheet-mysql/
# http://pentestmonkey.net/cheat-sheet/sql-injection/postgres-sql-injection-cheat-sheet
# http://atta.cked.me/home/sqlite3injectioncheatsheet
# https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/
# https://gist.githubusercontent.com/MattDMo/6cb1dfbe8a124e1ca5af/raw/a511e86dde7b3a70bdbd63b7ac3c98c32cd74277/ipy_repl.py
# https://gist.github.com/MattDMo/6cb1dfbe8a124e1ca5af
# http://atta.cked.me/home/sqlite3injectioncheatsheet
# https://github.com/unicornsasfuel/sqlite_sqli_cheat_sheet
# https://sqliteonline.com/
# http://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet
# http://ringzer0team.com:1008/?page=php://filter/convert.base64-encode/resource=/var/www/html/index.php
# https://www.branah.com/ascii-converter
# ALWAYS LOOK IN SOURCE CODE, COOKIES AND HEADERS!
# Case sensitivity in sql: https://dev.mysql.com/doc/refman/5.7/en/case-sensitivity.html
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import requests


class BrowserTool:

    def __init__(self):
        self.browser = None
        self.username = ""
        self.password = ""

    def stalenessOf(self, driver, element):
        try:
            element.is_enabled()
            return False
        except:
            return True 

    def wait_for_page_load_after_element_click(self, element, timeout=3):
        htmlElem = self.browser.find_element_by_tag_name("html")
        element.click()
        WebDriverWait(self.browser, timeout).until(lambda d: self.stalenessOf(d, htmlElem))

    def wait_for_page_load_after_refresh(self, timeout=3,accept_alert=False):
        htmlElem = self.browser.find_element_by_tag_name("html")
        self.browser.refresh()
        if accept_alert:
            self.browser.switch_to.alert.accept()
        WebDriverWait(self.browser, timeout).until(lambda d: self.stalenessOf(d, htmlElem))

    def remove_password_type(self):
        for e in self.browser.find_elements_by_name('password'):
            self.browser.execute_script("return arguments[0].setAttribute('type','text')",e)
        for e in self.browser.find_elements_by_name('new_password'):
            self.browser.execute_script("return arguments[0].setAttribute('type','text')",e)
        for e in self.browser.find_elements_by_name('pass'):
            self.browser.execute_script("return arguments[0].setAttribute('type','text')",e)

    def init(self):
        default_site = raw_input('Please enter the default url to access [https://github.com/tristandostaler/CTFTool]: ')
        if default_site == "":
            default_site = "https://github.com/tristandostaler/CTFTool"
        use_proxy = raw_input('Use proxy (eg. Burp) [Y/n]? ')
        if use_proxy.lower() != "n":
            proxyHost = raw_input('Please provide the proxy host [127.0.0.1]: ')
            if proxyHost == "":
                proxyHost = "127.0.0.1"
            proxyPort = raw_input('Please provide the proxy port [8080]: ')
            if proxyPort == "":
                proxyPort = "8080"
            fp = webdriver.FirefoxProfile()
            fp.set_preference("network.proxy.type", 1)
            fp.set_preference("network.proxy.http", proxyHost) #HTTP PROXY
            fp.set_preference("network.proxy.http_port", int(proxyPort))
            fp.set_preference("network.proxy.ssl", proxyHost) #SSL  PROXY
            fp.set_preference("network.proxy.ssl_port", int(proxyPort))
            fp.set_preference("network.proxy.ftp", proxyHost) #HTTP PROXY
            fp.set_preference("network.proxy.ftp_port", int(proxyPort))
            fp.set_preference('network.proxy.socks', proxyHost) #SOCKS PROXY
            fp.set_preference('network.proxy.socks_port', int(proxyPort))
            fp.update_preferences()
            self.browser = webdriver.Firefox(firefox_profile=fp)
        else:
            self.browser = webdriver.Firefox()
        self.browser.get(default_site)

    def login(self, form_control_name="form-control", form_control_index=0, username_element_name='username', password_element_name='password'):
        if self.username == "":
            self.username = raw_input('Please provide the username to use by default: ')
        if self.password == "":
            self.password = raw_input('Please provide the password to use by default: ')
        self.browser.find_element_by_name(username_element_name).send_keys(self.username)
        self.browser.find_element_by_name(password_element_name).send_keys(self.password)
        self.browser.find_elements_by_class_name(form_control_name)[form_control_index].click()

    #http://docs.python-requests.org/en/master/user/quickstart/
    def get_raw_request(self, url, payload=None, headers=None):
        if headers == None:
            headers = { 'user-agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0'}
        headers['Cookie'] = ""
        for cookie in self.browser.get_cookies():
            headers['Cookie'] = headers['Cookie'] + str(cookie['value']) + ";"
        if payload == None:
            r = requests.get(url)
        else:
            r = requests.get(url, params=payload)
        return r

    def post_raw_request(self, url, payload=None, headers=None):
        if headers == None:
            headers = { 'user-agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0'}
        headers['Cookie'] = ""
        for cookie in self.browser.get_cookies():
            headers['Cookie'] = headers['Cookie'] + str(cookie['value']) + ";"
        if payload == None:
            r = requests.post(url)
        else:
            r = requests.post(url, params=payload)
        return r