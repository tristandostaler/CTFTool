from .long_strings import *
from select import select
import sys
import time
import jsbeautifier
import ctypes, mmap
import io
from contextlib import redirect_stdout


def run_shellcode_return_string(shellcode):
    print('Output will be redirected')
    with io.StringIO() as buf, redirect_stdout(buf):
        run_shellcode(shellcode)
        output = buf.getvalue()
        #TODO

def run_shellcode(shellcode):
    # Convert string to bytes object. Differs between Python2 and Python3
    if sys.version_info >= (3, 0):
        def b(string, charset='latin-1'):
            if isinstance(string, bytes) and not isinstance(string, str):
                return (string)
            else:
                return bytes(string, charset)
    else:
        def b(string):
            return bytes(string)

    def create_shellcode_function (shellcode_str):
        shellcode_bytes = b(shellcode_str)

        # Allocate memory with a RWX private anonymous mmap
        exec_mem = mmap.mmap(-1, len(shellcode_bytes),
                            prot = mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC,
                            flags = mmap.MAP_ANONYMOUS | mmap.MAP_PRIVATE)

        # Copy shellcode from bytes object to executable memory
        exec_mem.write(shellcode_bytes)

        # Cast the memory to a C function object
        ctypes_buffer = ctypes.c_int.from_buffer(exec_mem)
        function = ctypes.CFUNCTYPE( ctypes.c_int64 )(ctypes.addressof(ctypes_buffer))
        function._avoid_gc_for_mmap = exec_mem

        # Return pointer to shell code function in executable memory
        return function
    
    # Create a pointer to our shell code and execute it with no parameters
    create_shellcode_function(shellcode)()

def replace_elements_in_text(text, dict_of_elements):
    for k, v in dict_of_elements:
        text = text.replace(k,v)
    return text

def check_not_key_pressed(): #Inverse checking to ease programming
    # TODO fix this. Not working.
    # Temp fix:
    return True
    rlist, wlist, xlist = select([sys.stdin], [], [], 0.1)
    if rlist:
        return False
    else:
        return True

def show_exception(ex):
    template = "\tAn exception of type {0} occurred. Arguments:\n\t{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)

def print_banner_header():
    print(banner_header)
    #for i in range(3):
    #    for j in range(0,10):
    #        print('\r              ' + (' '*j*4) + ('o'*5) + (' '*(34-(j*4)+1)), end='')
    #        sys.stdout.flush()
    #        time.sleep(0.05)
    #    for j in range(0,10):
    #        print('\r              ' + (' '*(34-(j*4)+1)) + ('o'*5) + (' '*j*4), end='')
    #        sys.stdout.flush()
    #        time.sleep(0.05)
    #print('\r' + ' '*35)

def print_banner_footer():
    print(banner_footer)

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

