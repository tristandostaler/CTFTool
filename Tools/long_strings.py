banner_header = '''
 .d8888b.  88888888888 8888888888 88888888888                   888 
d88P  Y88b     888     888            888                       888 
888    888     888     888            888                       888 
888            888     8888888        888      .d88b.   .d88b.  888 
888            888     888            888     d88""88b d88""88b 888 
888    888     888     888            888     888  888 888  888 888 
Y88b  d88P     888     888            888     Y88..88P Y88..88P 888 
 "Y8888P"      888     888            888      "Y88P"   "Y88P"  888 
                                 
This is a nice CTF tool designed by Tristan Dostaler
    https://github.com/tristandostaler/CTFTool
'''

banner = '''

To print this banner again, please use the function:
    print_banner()

At the moment, it is only possible to interact with the website.
We can't yet bypass it like with burp.

To use this tool, start by defining a function that handles the logic of the page.
A typical use is to create a function that get's the page, search for an element
by it's id and verify the result. If the challenge is a GET, you only need 1 function,
if not, you need 2 (1 to acces, 1 to execute the logic).
Ex:
GET:
    def run_challenge_77_with_id(idText):
        browser.get('http://web.ringzer0team.com:13372/index.php?id=' + idText + '&s=' + hashlib.md5(idText).hexdigest())
        for l in browser.find_elements_by_tag_name('section'):
            if str(l.text).strip() != "" and 'User with ID' in str(l.text).strip():
                if 'exists on the database' in str(l.text).strip():
                    return True
                else:
                    return False
POST:
    def access_challenge_5():
        browser.get('https://ringzer0team.com/challenges/5')

    def run_challenge_5_with_text(text):
        print "Trying " + text
        #The username field is SQL injectable
        browser.find_element_by_name('username').send_keys(text)
        wait_for_page_load_after_element_click(browser.find_elements_by_class_name('form-control')[2])
        chalWrapperText = browser.find_element_by_class_name('alert-danger').text.encode('utf-8')
        if "Invalid username / password." in chalWrapperText:
            print "True"
            return True
        else:
            print "False"
            return False


To get a list of usefull function, use the function:
    get_usefull_functions()

A few things to always remember:

    - ALWAYS LOOK IN SOURCE CODE, COOKIES AND HEADERS!
    - When doing SQLi, always think about case sensitivity! (eg. COLLATE latin1_bin)
    - http://pentestmonkey.net/category/cheat-sheet/sql-injection
    - Remember to test the multibyte char SQLi trick

'''


usefull_function = ('''
THIS MIGHT NOT BE UP TO DATE. IF SO, PLEASE UPDATE THIS!
Usefull functions:
    print_banner()
        No args
        Print the welcome header

    replace_elements_in_text(text, dict_of_elements)
        text - the text to apply the modification to
        dict_of_elements - a dictionnary of key to replace by the value
        Function which return the initial text with keys replaced by values
            (Ex: replace_elements_in_text('ABC', [('A','a'),('B','b'),('C','c')]) => 'abc')

    show_exception(ex)
        ex - the exception object when catching an exception
        Function used to display some usefull info on an exception.
            Use this when try/catching!

    detect_dbms(func)
        func - the user defined function that handles the logic
        Function used to try to detect the DBMS

    dbms_detection_values(dbms)
        dbms - a DBMS enum value that indicates the dbms type (Ex: DBMS.MySQL)
        Print and returns an array of tests that is specific to the dbms

    try_default_SQLi_tests(func)
        func - the user defined function that handles the logic
        This function will try multiple payloads in different formats, 
            asking the user to skip or continue before every request
            so the user can manually determine if a test worked.

    all_256_character_as_hex_brute_force_substr(func, payload, letters_as_hex)
        func - the user defined function that handles the logic
        payload - the handcrafted payload for a specific SQLi 
            (Ex: ' and substr(select version()),1,[count])=[letters] -- )
        letters_as_hex - hex values of the starting letters already discovered
            (Ex: "414243")
        This function will bruteforce all the possibilities based on the hex values.
            (Ex: 0x414243 => 'ABC')

    all_256_character_as_char_brute_force_substr(func, payload, numbers_as_array=[])
        func - the user defined function that handles the logic
        payload - the handcrafted payload for a specific SQLi 
            (Ex: ' and substr(select version()),1,[count])=[letters] -- )
        numbers_as_array - An array of decimal values of letters already discovered
            (Ex: [65, 66, 67] => 'ABC')
        This function will bruteforce all the possibilities based on the decimal values.
            (Ex: concat(char(65),char(66),char(67)) => 'ABC' )

    general_brute_force_substr(func, payload, letters="", lower=False, upper=False, number=False, punct=False)
        func - the user defined function that handles the logic
        payload - the handcrafted payload for a specific SQLi 
            (Ex: ' and substr(select version()),1,[count])=[letters] -- )
        letters - a string of the letters already discovered
        lower - Switch. Bruteforce using lower characters?
        upper - Switch. Bruteforce using upper characters?
        number - Switch. Bruteforce using number characters?
        punct - Switch. Bruteforce using punctuation characters?
        This function will bruteforce all the possibilities based on the switchs.

    remove_password_type()
        No args
        Looks in the page for passwords fields and remove the type='password' so we can see the characters.
            Usefull when using the field manually and we want to see what we are doing.

    wait_for_page_load_after_element_click(element, timeout=3)
        element - element returned by the browser variable when finding something in the page
        timeout - timeout in seconds before returning
        This function is used when automaticaly clicking on an element so that we wait for the page to
            load before we interact with the page again. Does not always work but helps.
''')