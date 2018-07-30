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

print('='*30 + '  Starting to work on ' + node_name + '  ' + '='*30 + '\n')
logging.info('Connecting to %s in order to restart %s...', node_name)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(node_name, username=USER, password=PSWD)
channel = ssh.get_transport().open_session()
channel.exec_command(command)

if (ssh_shell.recv_ready()):
    resultMessage += ssh_shell.recv(9999)
    resultMessage += '\r\n'

ssh.get_transport().close()
ssh.close()
