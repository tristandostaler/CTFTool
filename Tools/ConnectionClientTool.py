import paramiko
from paramiko_expect import SSHClientInteraction
import getpass
import socket
from telnetlib import Telnet
from pwn import *


def create_ssh_connection(HOSTNAME, PORT = 22, USERNAME = '', PASSWORD=''):
    if not USERNAME:
        USERNAME = input("Username: ")
    if not PASSWORD:
        PASSWORD = getpass.getpass()
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=HOSTNAME, port=PORT, username=USERNAME, password=PASSWORD)
    return client

def interact_with_ssh_connection(client, prompt_line = '.*@.*:.*', TIMEOUT=60*30):
    with SSHClientInteraction(client, timeout=TIMEOUT, display=True) as interact:
        need_to_exit=False
        interact.expect(prompt_line)
        while not need_to_exit:
            data = input(">")
            if "exit" in data:
                need_to_exit = True
            interact.send(data)
            interact.expect(prompt_line)

def create_socket_connection(HOSTNAME, PORT = 1234):
    sock = socket.socket()
    sock.connect((HOSTNAME, PORT))
    return sock

def create_telnet_connection(HOSTNAME, PORT = 1234):
    sock = create_socket_connection(HOSTNAME, PORT)
    t = Telnet()
    t.sock = sock
    return t

def interact_with_socket(sock):
    print("Warning, this is not working 100%!!")
    need_to_exit=False
    while not need_to_exit:
        data = input(">")
        if "exit" in data:
            need_to_exit = True
        sock.send((data + '\n').encode())
        data = sock.recv(1024).decode()
        print(data)

def interact_with_telnet_connection(telnet):
    telnet.interact()

def create_pwntool_connection(HOSTNAME, PORT):
    r = remote(HOSTNAME, PORT)
    return r

def interact_with_pwntool_connection(pwnconnection):
    pwnconnection.interactive()

def print_pwntool_automation_example():
    print('''
client = create_pwntool_connection('2018shell.picoctf.com',27833)
client.recvregex(".*~/$.*")
client.sendline('cd secret')
client.recvregex(".*~/secret$.*")
client.sendline('ls')
client.recvregex(".*~/secret$.*")
client.sendline('rm intel_1')
client.recvregex(".*~/secret$.*")
client.sendline("echo 'Drop it in!'")
client.recvregex(".*~/secret$.*")
client.sendline("cd ..")
client.recvregex(".*~/$.*")
client.sendline("cd executables")
client.recvregex(".*~/executables$.*")
client.sendline("./dontLookHere")
client.recvregex(".*~/executables$.*")
client.sendline("whoami")
client.recvregex(".*~/executables$.*")
client.sendline("cd ..")
client.recvregex(".*~/$.*")
client.sendline("cd passwords")
client.recvregex(".*~/passwords$.*")
client.sendline("cp /tmp/TopSecret ./")
client.recvregex(".*~/passwords$.*")
client.sendline("cd ..")
client.recvregex(".*~/$.*")
client.sendline("cp /tmp/TopSecret ./passwords")
client.recvregex(".*~/$.*")
client.sendline("cd passwords")
client.recvregex(".*~/passwords$.*")
client.interactive()
''')