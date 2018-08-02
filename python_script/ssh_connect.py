# -*- coding: utf-8 -*-
import sys
import datetime
import argparse
import time
import paramiko
import re

HOST = '192.168.1.136'
USER = 'manager'
PSWD = 'friend'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PSWD)

cmdlist = ["show clock", "show user"]

#Login prompt and getting hostname. This method is invoke in shell.
channel = ssh.invoke_shell()
while not channel.recv_ready():
    time.sleep(1)
results = channel.recv(2048)
channel.send('enable\n')
while not channel.recv_ready():
    time.sleep(1)
results += channel.recv(2048)
channel.send('\n')
while not channel.recv_ready():
    time.sleep(1)
results2 = channel.recv(2048)
r = re.compile(r'\r')
ret = re.sub(r,'',results.decode('utf-8'))
host_temp = re.sub('\r\r\n','',results2.decode('utf-8'))
print(ret)

#Input command list.
for item in cmdlist:
    stdin, stdout, stderr = ssh.exec_command(item)
    print(host_temp + item)
    for line in stdout:
        print (line.strip('\n'))


ssh.close()
