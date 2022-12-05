#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from server import server

if __name__ == '__main__':
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
