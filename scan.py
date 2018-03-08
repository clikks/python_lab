#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'lux'

import sys
import getopt
import re
from socket import *

def showUsage():
    print(
        """
        Usage: {} [-h|-p] [--host|--port|--help] args...
        Example: {} --host xxx.xxx.xxx.xxx --port 22
                 {} -h xx.xx.xx.xx -p 22-100
        """.format(sys.argv[0], sys.argv[0], sys.argv[0])
        )


def scan(host, ports):
    if len(ports) == 1:
        pass
    elif len(ports) == 2:
        ports = range(int(ports[0]), int(ports[-1])+1)
        
    for port in ports:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(0.1)
        # print(host, port)
        result = sock.connect_ex((host, port))
        if result == 0:
            print('{} open'.format(port))
        else:
            print('{} closed'.format(port))

if __name__ == '__main__':
    host = None
    ports = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:", ["help", "host=", "port="])
    except getopt.GetoptError:
        showUsage()

    for op, value in opts:
        if op in ("--help"):
            showUsage()
            exit(1)
        elif op in ("-h", "--host"):
            pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            host = re.match(pattern, value)
            if not host:
                print("Parameter Error")
                exit(1)
            else:
                host = host.group()
        elif op in ("-p", "--port"):
            pattern = r'^\d{1,5}$|^\d{1,5}-\d{1,5}$'
            ports = re.findall(pattern, value)
            if not len(ports):
                print("Parameter Error")
                exit(0)
            ports = ports[0].split('-')
            for port in ports:
                if int(port) > 65535 or int(port) == 0:
                    print("Parameter Error")
                    exit(0)

    if host is None or ports is None:
        showUsage()
    scan(host, ports)

