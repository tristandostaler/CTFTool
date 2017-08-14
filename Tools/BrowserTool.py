import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import requests
import re
import os


class BrowserTool:

    def __init__(self, default_site="https://github.com/tristandostaler/CTFTool", proxyHost="127.0.0.1", proxyPort="8080", username="", password="", verbosity=0):
        self.default_site = default_site
        self.browser = None
        self.username = username
        self.password = password
        self.proxyHost = proxyHost
        self.proxyPort = proxyPort
        self.webdriver_proxies = {}
        self.verbosity = verbosity
        self.main_tab = None

    def get_actual_tab_name(self):
        return self.browser.current_window_handle.encode()

    def get_all_tabs(self):
        return self.browser.window_handles
    
    def change_to_tab_by_index(self, index):
        self.browser.switch_to_window(self.browser.window_handles[index])
    
    def change_to_tab_by_name(self, name):
        self.browser.switch_to_window(name)

    def create_new_tab(self, base_url="", auto_switch=True):
        actual_tab = self.get_actual_tab_name()
        self.browser.execute_script("window.open('" + base_url + "')")
        if auto_switch:
            self.change_to_tab_by_name(actual_tab)

    def get_page_source(self):
        return self.browser.page_source.encode()

    def get_substring_in_page_source(self, start_string, end_string=""):
        page_source = self.get_page_source()
        if end_string == "":
            return page_source[page_source.index(start_string):]
        else:
            return page_source[page_source.index(start_string):page_source.index(end_string)]
    
    def get_substring_from_given_source(self, source, start_string, end_string=""):
        if end_string == "":
            return source[source.index(start_string):]
        else:
            return source[source.index(start_string):source.index(end_string)]

    def replace_cookie(self, name, value):
        self.browser.delete_cookie(name)
        self.browser.add_cookie({"name": name, "value": value})
    
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
        #if self.default_site == "":
        #    self.default_site = input('Please enter the default url to access [https://github.com/tristandostaler/CTFTool]: ')
        #if self.default_site == "":
        #    self.default_site = "https://github.com/tristandostaler/CTFTool"
        #use_proxy = input('Use proxy (eg. Burp) [Y/n]? ')
        #if use_proxy.lower() != "n":
        #    self.proxyHost = input('Please provide the proxy host [127.0.0.1]: ')
        #    if self.proxyHost == "":
        #        self.proxyHost = "127.0.0.1"
        #    self.proxyPort = input('Please provide the proxy port [8080]: ')
        #    if self.proxyPort == "":
        #        self.proxyPort = "8080"
        if self.proxyHost != "":
            self.webdriver_proxies = {
                'http': 'http://' + self.proxyHost + ":" + self.proxyPort,
                'https': 'https://' + self.proxyHost + ":" + self.proxyPort,
                'ftp': 'ftp://' + self.proxyHost + ":" + self.proxyPort
                }
            fp = webdriver.FirefoxProfile()
            fp.set_preference("network.proxy.type", 1)
            fp.set_preference("network.proxy.http", self.proxyHost) #HTTP PROXY
            fp.set_preference("network.proxy.http_port", int(self.proxyPort))
            fp.set_preference("network.proxy.ssl", self.proxyHost) #SSL  PROXY
            fp.set_preference("network.proxy.ssl_port", int(self.proxyPort))
            fp.set_preference("network.proxy.ftp", self.proxyHost) #HTTP PROXY
            fp.set_preference("network.proxy.ftp_port", int(self.proxyPort))
            fp.set_preference('network.proxy.socks', self.proxyHost) #SOCKS PROXY
            fp.set_preference('network.proxy.socks_port', int(self.proxyPort))
            fp.update_preferences()
            self.browser = webdriver.Firefox(firefox_profile=fp)
        else:
            self.browser = webdriver.Firefox()
        self.main_tab = self.browser.current_window_handle
        self.browser.get(self.default_site)

    def login(self, form_control_name="form-control", form_control_index=2, username_element_name='username', password_element_name='password'):
        if self.username == "":
            self.username = input('Please provide the username to use by default: ')
        if self.password == "":
            self.password = input('Please provide the password to use by default: ')
        self.browser.find_element_by_name(username_element_name).send_keys(self.username)
        self.browser.find_element_by_name(password_element_name).send_keys(self.password)
        self.browser.find_elements_by_class_name(form_control_name)[form_control_index].click()

    #http://docs.python-requests.org/en/master/user/quickstart/
    def get_raw_request(self, url, send_to_browser=False, payload=None, headers={}):
        if headers == {}:
            headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'}
        for cookie in self.browser.get_cookies():
            headers['Cookie'] = (headers['Cookie'] if 'Cookie' in headers else "") + str(cookie['name']) + "=" + str(cookie['value']) + ";"
        if payload == None:
            r = requests.get(url, headers=headers)
        else:
            r = requests.get(url, headers=headers, params=payload, proxies=self.webdriver_proxies, verify=self.webdriver_proxies=={})
        if send_to_browser:
            self.send_result_to_browser(r)
        return r

    def post_raw_request(self, url, send_to_browser=False, payload=None, headers={}):
        if headers == {}:
            headers = { 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'}
        for cookie in self.browser.get_cookies():
            headers['Cookie'] = (headers['Cookie'] if 'Cookie' in headers else "") + str(cookie['name']) + "=" + str(cookie['value']) + ";"
        if payload == None:
            r = requests.post(url, headers=headers)
        else:
            r = requests.post(url, headers=headers,data=payload, proxies=self.webdriver_proxies, verify=self.webdriver_proxies=={})
        if send_to_browser:
            self.send_result_to_browser(r)
        return r

    def send_result_to_browser(self, request):
        clean = re.sub('[^\s!-~]', '', request.text.encode('utf8').replace('\n','<br/>').replace('"','\"'))
        realPath = os.path.realpath(__file__)
        dirPath = os.path.dirname(realPath)
        file_dir = dirPath + '/../Data';
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with open(file_dir + '/recent_request_response.html','w') as f:
            f.write(clean)
        self.browser.get("file:///" + file_dir + "/recent_request_response.html")
