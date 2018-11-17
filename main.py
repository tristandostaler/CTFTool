#!/usr/bin/env python3
# pip install selenium
# pip install ipython
# pip install jsbeautifier
# pip install requests
# also install https://github.com/mozilla/geckodriver/releases
# sudo mv geckodriver /usr/bin
# export PATH=$PATH:/usr/bin/geckodriver
# then run script
# Sources:
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
#
# Adding a git submodule: https://stackoverflow.com/questions/2140985/how-to-set-up-a-git-project-to-use-an-external-repo-submodule
#
# Notes:
# ALWAYS LOOK IN SOURCE CODE, COOKIES AND HEADERS!
# Case sensitivity in sql: https://dev.mysql.com/doc/refman/5.7/en/case-sensitivity.html
# Punch cart emulator: http://tyleregeto.com/article/punch-card-emulator

import sys
import time
import binascii
import hashlib
import argparse
import subprocess
import base64
from argparse import RawTextHelpFormatter
from IPython.terminal.embed import InteractiveShellEmbed
from Tools.utils import *
from Tools.BrowserTool import BrowserTool
import Tools.SQLiTool
import Tools.XSSTool
import Tools.CryptoTool


def main(args):
    initialise(args.url, args.proxy_host, args.proxy_port, args.username, args.password, args.verbosity)

def initialise(url="https://github.com/tristandostaler/CTFTool", proxy_host="127.0.0.1", proxy_port="8080", username="", password="", verbosity=0):
    print_banner_header()
    global allBrowserTool
    global mainBrowserTool
    mainBrowserTool = BrowserTool(default_site=url, proxyHost=proxy_host, 
        proxyPort=proxy_port, username=username, password=password, 
        verbosity=verbosity)
    allBrowserTool.append(mainBrowserTool)
    mainBrowserTool.init()
    #ctfTool.login()
    print_banner_footer()
    print("\nMain done")

def open_another_browser(default_site="https://github.com/tristandostaler/CTFTool", proxyHost="127.0.0.1", proxyPort="8080", username="", password="", verbosity=0):
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
    parser.add_argument("-N", "--no-interactive", action="store_true", default=False,
                    help="Optional switch. If set, the IPython interactive console will not start.")
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

    #Block: Uncomment when debugging using REPL
    #args.proxy_host = ""
    #args.proxy_port = ""
    #End Block

    main(args)
    if not args.no_interactive:
        banner = '*** Nested interpreter ***'
        exit_msg = '*** Back in main IPython. Call ipshell() to restart ***'
        ipshell = InteractiveShellEmbed(banner1=banner, exit_msg=exit_msg)
        ipshell.set_autoindent()
        ipshell()

