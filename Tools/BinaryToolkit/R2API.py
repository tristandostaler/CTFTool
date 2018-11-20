import r2pipe as R2p


class R2API:
    def __init__(self, debuggee, analyze = True):
        self.r2 = R2p.open(debuggee)
        if analyze:
            self.r2.cmd('aaa')

    def run_cmd(self, command):
        return self.r2.cmd(command)

    def analyze(self):
        self.run_cmd('aa')

    def set_breakpoint(self, address):
        return self.run_cmd("db " + address)

    def disas_function(self, fn_name):
        return self.run_cmd("pdf @" + fn_name)

    def run(self):
        return self.run_cmd("dc")

    def run_until(self, address):
        return self.run_cmd("dcu " + address)

    def get_functions(self):
        return

    def info(self):
        return self.run_cmd("i")

    def all_info(self):
        return self.run_cmd("ia")

    def resources(self):
        return self.run_cmd("iR")

    def sections(self):
        return self.run_cmd("iS")

    def symbols(self):
        return self.run_cmd("is")

    def headers(self):
        return self.run_cmd("ih")

    def other_info(self, which_info):
        return self.run_cmd("i" + which_info)

    def flags(self):
        return self.run_cmd("f")

    def flag(self, type):
        return self.run_cmd("f" + type)

    def get_register(self, reg):
        return self.run_cmd("dr " + reg)

    def get_registers(self):
        return self.run_cmd("dr")

    def set_register(self, reg, value):
        return self.run_cmd("dr " + reg + '=' + value)

    def __del__(self):
        self.r2.quit()

r = R2API('./Something', analyze=True)
dis_main = r.disas_function('sym.main')
print(dis_main)