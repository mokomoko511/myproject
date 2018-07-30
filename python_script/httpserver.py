import http.server
import socketserver
import os
import sys
import argparse


def get_args():
    #help ArgumentParser
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--portnumber', help='Set listen port, default 8000.',  type=int)
    parser.add_argument('-f', '--dirfolder', help='Set folder path, default current directory.',  type=str)
    args = parser.parse_args()
    return(args)

def main():
    args = get_args()
    # print(port)
    port=args.portnumber
    dirfolder=args.dirfolder
    if port is None:
        port=8000

    if dirfolder is not None:
        web_dir = os.path.join(os.path.dirname(__file__), dirfolder)
        os.chdir(web_dir)
    else:
        web_dir = os.path.join(os.path.dirname(__file__), '.')
        os.chdir(web_dir)

    print("HTTP server starting...Please close this window to stop http server.")
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    print("serving at port", port)
    print("dirfolder is ", dirfolder)

    httpd.serve_forever()

if __name__ == '__main__':
    main()
