# -*- coding: utf-8 -*-

import sys
import telnetlib
import socket
import datetime
import argparse
import random
import codecs
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
        print("Connetion timeout. Please check IPAddress." )
        input("Please input any key...")
        sys.exit()

    print("telnet connection successful. Start logging after login..." + "\n")
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
        print("Cannot login. Please check username or password.")
        input("Please input any key...")
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
        input("Please input any key...")
        sys.exit()
    # tn.write(("exit" + "\n").encode('ascii'))
    tn.write(("\n").encode('ascii'))
    ret+=tn.read_until(wait_hostname).rstrip()
    tn.read_very_lazy()
    sleep(1)
    print("\n" + "Completed get log. Close connection...")
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

    ipaddr=args.ipaddress
    user=args.username
    passwd=args.password
    cmdlist=args.cmdlist
    logfolder=args.logfolder
    logfilename=args.logfilename

    telnet_main(ipaddr, user, passwd, cmdlist, logfolder, logfilename)

if __name__ == '__main__':
    main()
