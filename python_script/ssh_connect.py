# -*- coding: utf-8 -*-
import sys
import datetime
import argparse

import paramiko

HOST = '192.168.1.136'
USER = 'manager'
PSWD = 'friend'
LOG_FILE='log.txt'

logger = paramiko.util.logging.getLogger()
paramiko.util.log_to_file(LOG_FILE)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, username=USER, password=PSWD)

#output+=stdout.read()
#stdin, stdout, stderr = ssh.exec_command('show clock')
#output+=stdout.read()
#cmdlist = ["show clock\n", "show user\n"]
#output=stdout.read()
#print(output)
stdin, stdout, stderr = ssh.exec_command('enable')

stdin, stdout, stderr = ssh.exec_command('show run | grep hostname')
# for line in stdout:
#     if line == ' ':
#       hostname="awplus"
#
#     hostname=line.strip("hostname"+"\s+")
#     print(hostname)
#     print (line.strip('\n'))



#for each in cmdlist:
#stdin.write('show clock\n')
#stdin.flush()
#  print(stdout.readlines())
#print(stdout.read())

#print '\n'.join(stdout.readlines())

#for line in stdout:
#    print (line.strip('\n'))

#stdin, stdout, stderr = ssh.exec_command('show run | grep hostname')
#for line in stdout:
#    if line == ' ':
#      hostname="awplus"

#    hostname=line.strip("hostname"+"\s")
#    print(hostname)
#    print (line.strip('\n'))

stdin, stdout, stderr = ssh.exec_command('show clock')
for line in stdout:
    print (line.strip('\n'))

stdin, stdout, stderr = ssh.exec_command('show run')
for line in stdout:
    print (line.strip('\n'))

ssh.close()
