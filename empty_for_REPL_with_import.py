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



