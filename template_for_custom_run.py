def other_function_to_use():
    print("Nothing yet")
    CTFTool.browser.get("http://example.com")

def custom_login():
    login(form_control_name="form-control", form_control_index=2)

if __name__ == "__main__":
    import sys
    import time
    if not sys.flags.interactive:
        print("Run this script in python or IPython interactive with [i]python -i scriptName.py for a better experience!")
        time.sleep(5)

    #TODO fix this
    from CTFTool import * 
    import CTFTool
    main() 

