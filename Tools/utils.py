from long_strings import *
from select import select
import sys
import time
import jsbeautifier


def replace_elements_in_text(text, dict_of_elements):
    for k, v in dict_of_elements:
        text = text.replace(k,v)
    return text

def check_not_key_pressed(): #Inverse checking to ease programming
    rlist, wlist, xlist = select([sys.stdin], [], [], 0.1)
    if rlist:
        return False
    else:
        return True

def show_exception(ex):
    template = "\tAn exception of type {0} occurred. Arguments:\n\t{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print message

def print_banner():
    print(banner_header)
    for i in range(3):
        for j in range(0,10):
            print '\r              ' + (' '*j*4) + ('o'*5) + (' '*(34-(j*4)+1)),
            sys.stdout.flush()
            time.sleep(0.05)
        for j in range(0,10):
            print '\r              ' + (' '*(34-(j*4)+1)) + ('o'*5) + (' '*j*4),
            sys.stdout.flush()
            time.sleep(0.05)
    print('\r' + ' '*35)
    print(banner)

def get_usefull_functions():
    print(usefull_function)

def beautify_javascript_from_file(file):
    return jsbeautifier.beautify_file(file)

def beautify_javascript_from_text(text):
    return jsbeautifier.beautify(text)

def header_string_to_dict(header_string):
    header_dict = {}
    for h in header_string.split('\n'):
        if 'Content-Length' not in h and 'POST' not in h and 'GET' not in h:
            header_dict[h.split(': ')[0]] = h.split(': ')[1]
    return header_dict

