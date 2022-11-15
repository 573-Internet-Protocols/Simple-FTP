#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

from checksum import checksum


def server(port, file_name, p):
    port = 7735
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss.bind(('', port))
    content = b''
    i = 0
    while True:
        data, client_address = ss.recvfrom(2048)
        if data:
            print(len(data))
            sequence_number = data[0:32]
            check_sum = data[32:48]
            pack_field = data[48:64]
            d = data[64:]
            new_check_sum = checksum(sequence_number + pack_field + d)
            new_check_sum = '{0:016b}'.format(new_check_sum).encode()
            if new_check_sum == check_sum:
                content += d
                print('received', i, len(d))
                i += 1
    return None
