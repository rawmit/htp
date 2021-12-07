#!/usr/bin/env python
from os import makedirs, listdir,path
import argparse
from re import search
import socket
from time import sleep

parser = argparse.ArgumentParser(description="List of htp aguments",usage="python3 htp.py -h For see features")
parser.add_argument("--password-list",type=str,help='Path of password-list file')
parser.add_argument("-scan",type=str,help="Path of file for save scanned http and https proxies to the file")
parser.add_argument("-http",type=str,help="Path of file for save scanned http proxies to the file")
parser.add_argument("-https",type=str,help="Path of file for save scanned https proxies to the file")
parser.add_argument("-config",type=str,help='Path of config file',default='htp-data/config.ini')
parser.add_argument("-out",type=str,help='Path of file to save output',default='htp-data/output.pwl')
parser.add_argument("-l",type=str,nargs='?',const=1,help='Show log')
args = parser.parse_args()

# Ports to be scanned for http proxy servers
ports = [8080,80,3128,3389,3129,999,8000,3256,4153,5678]
# Ports to be scanned for https proxy servers
sports = [8080,3128,80,3129,999,84,83,82,5678,4153,9999]

if 'htp-data' not in listdir():
    makedirs('htp-data')
ip_list = 'htp-data/ip-list.il'
confh = """#Example methods:
[s=]*[e=#]
[s=#]*[e=#]
[s=-]*[e=*]
[s=@]*[e=!]"""

if args.scan:
    httpf = open(str(args.scan.split('.')[-2])+'-http.'+args.scan.split('.')[-1],'w')
    httpf.close()
    httpsf = open(str(args.scan.split('.')[-2])+'-https.'+args.scan.split('.')[-1],'w')
    httpsf.close()
if args.http:
    httpf = open(str(args.http),'w')
    httpf.close()
if args.https:
    httpf = open(str(args.https),'w')
    httpf.close()

def main():
    if not args.password_list is None:
        password_list_gen()
    elif not args.scan is None or not args.http is None or not args.https is None:
        scan_ip()

def scan_ip():
    if not path.isfile(ip_list):
        raise KeyError(f"{ip_list} file is not found")
    with open(ip_list,'r') as f:
        r = f.readlines()
        f.close()
    for iprange in r:
        iprange = iprange.split(",")
        if isinstance(iprange, list):
            if isinstance(iprange[0].split('.'), list) and isinstance(iprange[1].split('.'), list):
                if len(iprange[0].split('.')) == 4 and len(iprange[1].split('.')) == 4:
                    if iprange[1][-1]=='\n':iprange[1]=iprange[1][:-1]
                    tmprange = [iprange[0].split('.'),iprange[1].split('.')]
                    n = [int(it) for it in tmprange[0]]
                    s = [str(it) for it in n]
                    while True:
                        s = [str(it) for it in n]
                        if s == tmprange[1]:
                            break
                        scan(ip='.'.join(s))
                        r0=True
                        if n[3] >= 255: 
                            n[2]=n[2]+1
                            n[3] = 0
                            r0=False
                        if n[2] >= 255: 
                            n[1]=n[1]+1
                            n[2] = 0
                        if n[1] >= 255: 
                            n[0]=n[0]+1
                            n[1] = 0
                        if n[0] >= 255 and n[1] == 255 and n[2] == 255 and n[3] == 255:
                            break
                        if r0:
                            n[3]+=1
    print('htp done.')

def password_list_gen():
    if not path.isfile(args.password_list):
        raise KeyError(f"{args.password_list} file is not found")
    if not path.isfile(args.config):
        while True:
            ans = input(f"Config file is not exists in: {args.config}, do you want to use default configs [y/n]? ").lower()
            if ans == 'y' or ans == 'yes':
                with open(args.config,'w') as file:
                    file.write(confh)
                    file.close()
                    break
            elif ans == 'n' or ans == 'no':
                return exit(0)
    with open(args.config,'r') as file:
        c = file.readlines()
        file.close()
    methods = []
    print(f"Reading {args.config}")
    for item in c:
        t = search(r"\[s=(.*)?\]\*\[e=(.*)?\]",item)
        if not t is None:
            methods.append(t.groups())
    with open(args.password_list,'r') as file:
        c = file.readlines()
        file.close()
    print(f"Reading {args.password_list}")
    out = []
    for item in c:
        if item[-1:] == '\n':item=item[:-1]
        for method in methods:
            out.append(f"{method[0]}{item}{method[1]}\n")
    with open(args.out,'w') as file:
        file.writelines(out)
        file.close()
    print(f"htp Done. output saved in {args.out}")
    return exit(0)

def scan(ip):
    if args.http or args.scan:
        if args.l:print("scanning http",ip)
        for port in ports:            
            sleep(0.1)
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(10)
            try:
                s.connect((f"{ip}",port))
                s.send("""GET / HTTP/1.1\r\nHost:www.google.com\r\n\r\n""".encode())
                d = s.recv(4096)
                if not search(r"HTTP/1.(1|0) 200 (Connection established|OK)",str(d)) is None:
                    if args.l:print("HTTP Hit:",ip,port)
                    if args.scan:
                        with open(str(args.scan.split('.')[-2])+'-http.'+args.scan.split('.')[-1],'a') as httpf:
                            httpf.write(str(ip)+f':{port}\n')
                            httpf.close()
                    if args.http:
                        with open(str(args.http),'a') as httpf:
                            httpf.write(str(ip)+f':{port}\n')
                            httpf.close()
            except:pass
            s.close()
    if args.https or args.scan:
        if args.l:print("scanning https",ip)
        for port in sports:            
            sleep(0.1)
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(15)
            try:
                s.connect((f"{ip}",port))
                s.send("CONNECT google.com:443 HTTP/1.0\r\n\r\n".encode())
                d = s.recv(4096)
                if not search(r"HTTP/1.(1|0) 200 (Connection established|OK)",str(d)) is None:
                    if args.l:print("HTTPS Hit:",ip,port)
                    if args.scan:
                        with open(str(args.scan.split('.')[-2])+'-https.'+args.scan.split('.')[-1],'a') as httpf:
                            httpf.write(str(ip)+f':{port}\n')
                            httpf.close()
                    if args.https:
                        with open(str(args.https),'a') as httpf:
                            httpf.write(str(ip)+f':{port}\n')
                            httpf.close()
            except:pass
            s.close()

if __name__ == '__main__':
    main()
