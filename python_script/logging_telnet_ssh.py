# -*- coding: utf-8 -*-

import sys, argparse, re, random, codecs
import telnetlib, socket
import datetime, time
import paramiko
from time import sleep


def telnet_main(ipaddr, user, passwd, cmdlist, logfolder, logfilename):

    #Import cmdlists
    cmds = []
    for line in open(cmdlist, 'r').readlines():
        cmds.append(line.strip())

    print("Connecting to " + ipaddr)
    try:
        tn = telnetlib.Telnet(ipaddr,23,30)
    except socket.timeout:
        print("Connetion timeout. Please check following IPAddress : " + ipaddr )
        input("Please any key to continue...")
        sys.exit()

    print(ipaddr + " connect to telnet successful. Start logging after login..." + "\n")
    try:
        ret=tn.read_until(b"login:")
        tn.write((user+"\n").encode('ascii'))
        ret+=tn.read_until(b"Password:")
        tn.write((passwd+"\n").encode('ascii'))
        ret+=tn.read_until(b">")
        tn.write(("enable"+"\n").encode('ascii'))
        ret+=tn.read_until(b"#")
        #Get hostname
        tn.write(("\n").encode('ascii'))
        tn.read_until(b"\n")
        wait_hostname=tn.read_until(b"#")
        #print(wait_hostname)
        hostname_get=(wait_hostname.strip(b"#").decode('ascii'))
        print("hostname : " + hostname_get)
        tn.write(("terminal length 0"+"\n").encode('ascii'))
        ret+=tn.read_until(b"#")
    except EOFError:
        print("Cannot login successfully. Please check username or password of " + ipaddr)
        input("Please any key to continue...")
        sys.exit()

    #Input commands from cmds list
    try:
        for cmdline in range(len(cmds)):
            cmditem = cmds[cmdline]
            print("The next get log for : " + cmditem)
            tn.write((cmditem + "\n").encode('ascii'))
            ret+=tn.read_until(wait_hostname).rstrip()
            sleep(0.005)
            tn.read_very_lazy()
        # print(ret)
    except EOFError:
        print("Something went wrong. Please retry host to " + ipaddr)
        input("Please any key to continue...")
        sys.exit()
    # tn.write(("exit" + "\n").encode('ascii'))
    tn.write(("\n").encode('ascii'))
    ret+=tn.read_until(wait_hostname).rstrip()
    tn.read_very_lazy()
    sleep(1)
    print("\n" + "Completed get logging. Close connection...")
    tn.close()
    ret+=tn.read_all()

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
    try:
        ret2=ret.decode('ascii')
    except UnicodeDecodeError:
        ret2=ret.decode('ascii', errors='ignore')

    ret2=ret2.replace('\r','')
    fp.write(ret2)
    fp.close()


def ssh_main(ipaddr, user, passwd, cmdlist, logfolder, logfilename):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ipaddr, username=user, password=passwd)
    except:
        print("Connetion timeout. Please check following IPAddress : " + ipaddr)
        input("Please any key to continue...")
        sys.exit()

    print(ipaddr + " connect to ssh successful. Start logging..." + "\n")

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
    try:
        for item in cmds:
            stdin, stdout, stderr = ssh.exec_command(item)
            ret+=host_temp + item + '\n'
            print('excute command : ' +  item)
            for line in stdout:
                ret+=line
                #print(ret)
    except:
        print("Something went wrong. Please retry host to " + ipaddr)
        input("Please any key to continue...")
        sys.exit()

    print("\n" + "Completed get logging. Close connection...")
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

    #Select connection method, Default is telnet.
    parser.add_argument('-t', '--telnet', help='Set telnet connection method, telnet is default.',action='store_const', const=True, default=True)
    parser.add_argument('-s', '--ssh', help='Set ssh connection method',action='store_const', const=True, default=False)
    parser.add_argument('-f', '--logfolder', help='Set the log folder',  type=str)
    parser.add_argument('-l', '--logfilename', help='Default logfile name "<hostname>_<date>", you can defined the logfilename',  type=str)

    args = parser.parse_args()
    return(args)

def main():
    args = get_args()

    ipaddr=args.ipaddress
    user=args.username
    passwd=args.password
    cmdlist=args.cmdlist
    logfolder=args.logfolder
    logfilename=args.logfilename

    if args.ssh == True:
        ssh_main(ipaddr, user, passwd, cmdlist, logfolder, logfilename)
    else:
        telnet_main(ipaddr, user, passwd, cmdlist, logfolder, logfilename)

if __name__ == '__main__':
    main()
