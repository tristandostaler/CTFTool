from IPython import embed
import sys
import time
import binascii
import hashlib
from utils import *
from BrowserTool import BrowserTool
import SQLiTool
import XSSTool


def main():
    global browserTool
    browserTool = BrowserTool()
    print_banner()
    browserTool.init()
    #ctfTool.login()
    print("\nMain done")

browserTool = None

if __name__ == "__main__":
    main()
    embed()
