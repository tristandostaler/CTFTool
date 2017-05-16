import CTFTool
from IPython import embed


def other_function_to_use(browser):
    print("Nothing yet")
    #CTFTool.SQLiTool.general_brute_force_substr(...)
    browser.get("http://example.com")

def custom_login():
    login(form_control_name="form-control", form_control_index=2)

def main():
    global browserTool
    browserTool = CTFTool.BrowserTool()
    browserTool.init()

browserTool = None

if __name__ == "__main__":
    # This template does not work well in the same directory
    #   as CTFTool. This is only a template.a
    #   Use main.py instead if you want to run CTFTool!
    main()
    embed()

