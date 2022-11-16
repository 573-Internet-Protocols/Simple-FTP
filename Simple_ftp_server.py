#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from client import client
from server import server

if __name__ == '__main__':
    if len(sys.argv) == 6:
        try:
            server_host_name = sys.argv[1]
            server_port = int(sys.argv[2])
            file_name = sys.argv[3]
            N = int(sys.argv[4])
            MSS = int(sys.argv[5])
            client(server_host_name, server_port, file_name, N, MSS)
        except Exception as e:
            print(e)
            print("Usage: Simple_ftp_server server-host-name server-port# file-name N MSS")
            sys.exit(1)
    elif len(sys.argv) == 4:
        try:
            port = int(sys.argv[1])
            file_name = sys.argv[2]
            p = float(sys.argv[3])
            server(port, file_name, p)
            assert p < 1, "p must be less than 1"
            assert p > 0, "p must be greater than 0"
        except Exception as e:
            print(e)
            print("Usage: Simple_ftp_server port# file-name p")
            sys.exit(1)
    else:
        print("Usage: Simple_ftp_server server-host-name server-port# file-name N MSS")
        print("Usage: Simple_ftp_server port# file-name p")
        sys.exit(1)
