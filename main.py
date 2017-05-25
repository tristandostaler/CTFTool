from IPython import embed
import sys
import time
import binascii
import hashlib
import argparse
from argparse import RawTextHelpFormatter
from Tools.utils import *
from Tools.BrowserTool import BrowserTool
import Tools.SQLiTool
import Tools.XSSTool
import Tools.CryptoTool


def main(args):
    print_banner_header()
    global allBrowserTool
    global mainBrowserTool
    mainBrowserTool = BrowserTool(default_site=args.url, proxyHost=args.proxy_host, 
        proxyPort=args.proxy_port, username=args.username, password=args.password, 
        verbosity=args.verbosity)
    allBrowserTool.append(mainBrowserTool)
    mainBrowserTool.init()
    #ctfTool.login()
    print_banner_footer()
    print("\nMain done")

def open_another_browser(default_site="https://github.com/tristandostaler/CTFTool", proxyHost="127.0.0.10", proxyPort="8080", username="", password="", verbosity=0):
    global allBrowserTool
    browserTool = BrowserTool(default_site,proxyHost,proxyPort,username,password,verbosity)
    allBrowserTool.append(browserTool)
    browserTool.init()

def parseArgs():
    parser = argparse.ArgumentParser(description=Tools.long_strings.banner_header, formatter_class=RawTextHelpFormatter)
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                    help="Increase output verbosity")
    parser.add_argument("-u", "--url", action="store", default="https://github.com/tristandostaler/CTFTool",
                    help="The default website to open on load")
    parser.add_argument("-o", "--proxy-host", action="store", default="127.0.0.1",
                    help="The proxy host to use. Ignored when --no-proxy")
    parser.add_argument("-p", "--proxy-port", action="store", default="8080",
                    help="The proxy port to use. Ignored when --no-proxy")
    parser.add_argument("--no-proxy", action="store_true",
                    help="Switch. Used to ignore proxy settings")
    parser.add_argument("-i", "--username", action="store", default="",
                    help="Optional. Username to use when calling the login function")
    parser.add_argument("-d", "--password", action="store", default="",
                    help="Optional. Password to use when calling the login function")
    args = parser.parse_args()
    if args.no_proxy:
        args.proxy_host = ""
        args.proxy_port = ""
    elif not args.no_proxy and (args.proxy_host == "" or args.proxy_port == ""):
        print("Arguments proxyHost and proxyPort are mandatory if the switch --no-proxy is not used.")
        exit()
    return args

allBrowserTool = list()
mainBrowserTool = None

if __name__ == "__main__":
    args = parseArgs()
    main(args)
    embed()

