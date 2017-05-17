from IPython import embed
import sys
import time
import binascii
import hashlib
from Tools.utils import *
from Tools.BrowserTool import BrowserTool
import Tools.SQLiTool
import Tools.XSSTool


def main():
    print_banner()
    global allBrowserTool
    global mainBrowserTool
    mainBrowserTool = BrowserTool()
    allBrowserTool.append(mainBrowserTool)
    mainBrowserTool.init()
    #ctfTool.login()
    print("\nMain done")

def open_second_browser():
    global allBrowserTool
    browserTool = BrowserTool()
    allBrowserTool.append(browserTool)
    browserTool.init()

allBrowserTool = list()
mainBrowserTool = None

if __name__ == "__main__":
    main()
    embed()
