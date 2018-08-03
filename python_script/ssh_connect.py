# -*- coding: utf-8 -*-
import sys
import datetime
import argparse
import time
import paramiko
import re

def ssh_main(ipaddr, user, passwd, cmdlist, logfolder, logfilename):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ipaddr, username=user, password=passwd)
    except socket.timeout:
        print("Connetion timeout. Please check IPAddress." )
        input("Please input any key...")
        sys.exit()

    print("ssh connection successful. Start logging..." + "\n")

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
    hostname_get=(host_temp.strip("#"))
    #Import cmdlists
    cmds = []
    for line in open(cmdlist, 'r').readlines():
        cmds.append(line.strip())

    #Input command list.
    for item in cmds:
        stdin, stdout, stderr = ssh.exec_command(item)
        ret+=host_temp + item + '\n'
        print('excute comand : ' +  item)
        for line in stdout:
            ret+=line
            #ret+=(line.strip('\n'))
            #print(ret)

    print("\n" + "Completed get log. Close connection...")
    ssh.close()

    #writing result to log file
    if logfilename is not None:
        if logfolder is not None:
            print(logfilename)
            filename=logfilename
        else:
            print(logfolder + logfilename)
            filename="%s%s" % (logfolder,logfilename)
    elif logfolder is not None:
        print(logfolder)
        now = datetime.datetime.now()
        filename = "%s%s_%i%.2i%.2i_%.2i%.2i%.2i.txt" % (logfolder,hostname_get,now.year,now.month,now.day,now.hour,now.minute,now.second)
    else:
        now = datetime.datetime.now()
        filename = "%s_%i%.2i%.2i_%.2i%.2i%.2i.txt" % (hostname_get,now.year,now.month,now.day,now.hour,now.minute,now.second)

    #If the log string was not ascii, that log line ignore.
    fp=open(filename,"w")
    # try:
    #     ret2=ret.decode('ascii')
    # except UnicodeDecodeError:
    #     ret2=ret.decode('ascii', errors='ignore')
    #print(ret)
    fp.write(ret)
    fp.close()

def get_args():
    #help ArgumentParser
    parser = argparse.ArgumentParser()
    if sys.stdin.isatty():
        parser.add_argument("ipaddress", help="please set ipaddress", type=str)
        parser.add_argument("username", help="set username", type=str)
        parser.add_argument("password", help="set password", type=str)
        parser.add_argument("cmdlist", help="set command line list file",type=str)

    parser.add_argument('-f', '--logfolder', help='Set the log folder',  type=str)
    parser.add_argument('-l', '--logfilename', help='Default logfile name "<hostname>_<date>", you can defined the logfilename',  type=str)

    args = parser.parse_args()
    return(args)

def main():
    args = get_args()

    # ipaddr=args.ipaddress
    # user=args.username
    # passwd=args.password
    # cmdlist=args.cmdlist
    ipaddr='192.168.1.136'
    user='manager'
    passwd='friend'
    cmdlist='G:\myproject\python_script\cmdlist.txt'
    logfolder=args.logfolder
    logfilename=args.logfilename

    ssh_main(ipaddr, user, passwd, cmdlist, logfolder, logfilename)

if __name__ == '__main__':
    main()
