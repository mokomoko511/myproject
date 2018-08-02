# -*- coding: utf-8 -*-
import sys
import datetime
import argparse
import paramiko
import logging
import select

node_name = '192.168.1.136'
USER = 'manager'
PSWD = 'friend'
LOG_FILE='log.txt'
command = "show clock"
logger = logging.getLogger(__name__)

import time
import logging
from paramiko import AutoAddPolicy,SSHClient,RSAKey

hostname = 'HostName or IPAddress'
key_file = "id_rsa.txt"
# ki=RSAKey.from_private_key_file(key_file,password='PASSPHRAS')
#paramiko.SSHClient()
client = SSHClient()
#Windowsから接続する場合
client.set_missing_host_key_policy( AutoAddPolicy())
#client.get_host_keys().add(hostname , 'ssh-rsa', ki)
client.connect(node_name, username=USER, password=PSWD)
channel = client.invoke_shell()
while not channel.recv_ready():
    time.sleep(1)
results = channel.recv(2048)

channel.send('enable\n')
while not channel.recv_ready():
    time.sleep(1)
results += channel.recv(2048)

channel.send('ter len 0\n')
while not channel.recv_ready():
    time.sleep(1)
results += channel.recv(2048)
#日本語はつらいよねー　
channel.send('show platform full\n')

while not channel.recv_ready():
    time.sleep(1)
results += channel.recv(2048)
channel.send('show run\n')
while not channel.recv_ready():
    time.sleep(1)
results += channel.recv(2048)
#results はこのままだと、エスケープシーケンス（色）が入っている
print(results.decode('utf-8'))

import re
r = re.compile(rb'\x1b\[.*?m\[?')
print(re.sub(r,'',results))
client.close()
