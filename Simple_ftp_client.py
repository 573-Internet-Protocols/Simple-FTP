#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from client import client

if __name__ == '__main__':
    try:
        server_host_name = sys.argv[1]
        server_port = int(sys.argv[2])
        file_name = sys.argv[3]
        N = int(sys.argv[4])
        MSS = int(sys.argv[5])
        client(server_host_name, server_port, file_name, N, MSS)
    except Exception as e:
        print(e)
        print("Usage: Simple_ftp_client server-host-name server-port# file-name N MSS")
        sys.exit(1)
