# CTFTool
A tool to ease CTFs

This tool has been designed by Tristan Dostaler


Windows is supported but the setup.sh and post_setup.sh has only been tested on Ubuntu.
To install everything on Ubuntu, first run setup.sh.
	Then, download the right version: https://github.com/mozilla/geckodriver/releases
	uncrompress and run ./post_setup.sh


To use this tool, you have 2 options:
- Run the main.py and use the provided IPython console to create and run functions.
- Use the provided template and start by defining a function that handles the logic of the page.

For both of these options, you can use SublimeREPL to 
	create functions and run them using CTRL + , S (CTRL and ',' then S)

	A typical use is to create a function that get's the page, search for an element
	by it's id and verify the result. If the challenge is a GET, you only need 1 function,
	if not, you need 2 (1 to acces the challenge page, 1 to execute the logic).
	Ex:
	GET:
	    def run_challenge_77_with_id(idText):
	        mainBrowserTool.browser.get('http://web.ringzer0team.com:13372/index.php?id=' + idText + '&s=' + hashlib.md5(idText).hexdigest())
	        for l in mainBrowserTool.browser.find_elements_by_tag_name('section'):
	            if str(l.text).strip() != "" and 'User with ID' in str(l.text).strip():
	                if 'exists on the database' in str(l.text).strip():
	                    return True
	                else:
	                    return False
	POST:
	    def access_challenge_5():
	        mainBrowserTool.browser.get('https://ringzer0team.com/challenges/5')

	    def run_challenge_5_with_text(text):
	        print "Trying " + text
	        #The username field is SQL injectable
	        mainBrowserTool.browser.find_element_by_name('username').send_keys(text)
	        wait_for_page_load_after_element_click(mainBrowserTool.browser.find_elements_by_class_name('form-control')[2])
	        chalWrapperText = mainBrowserTool.browser.find_element_by_class_name('alert-danger').text.encode('utf-8')
	        if "Invalid username / password." in chalWrapperText:
	            print "True"
	            return True
	        else:
	            print "False"
	            return False
