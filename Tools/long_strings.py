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
You can find multiple example on how to use this tool here:
       https://github.com/tristandostaler/CTFTool
'''

banner_footer = '''

To get a list of usefull function, use the function:
    Tools.utils.get_usefull_functions()

A few things to always remember:

    - ALWAYS LOOK IN SOURCE CODE, COOKIES AND HEADERS!
    - When doing SQLi, always think about case sensitivity! (eg. COLLATE latin1_bin)
    - http://pentestmonkey.net/category/cheat-sheet/sql-injection
    - Remember to test the multibyte char SQLi trick
        (http://stackoverflow.com/questions/5741187/sql-injection-that-gets-around-mysql-real-escape-string/12118602)

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
            (Ex: ' and substr((select version()),1,[count])=[letters] -- )
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