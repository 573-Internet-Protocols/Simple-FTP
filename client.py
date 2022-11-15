#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket

from checksum import checksum

packet_indicator = '0101010101010101'


def client(server_host_name, server_port, file_name, n, mss):
    server_port = 7735
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    f = open(file_name, 'rb')
    data = f.read()
    size = mss
    data_list = [data[i:i + size] for i in range(0, len(data), size)]

    segment_list = get_all_segments(data_list)
    index = 0
    for segment in segment_list:
        print('send', index)
        index += 1
        cs.sendto(segment, (server_host_name, server_port))
    cs.close()
    return None


def get_all_segments(data_list):
    index = 0
    segment_list = []
    for d in data_list:
        sequence_number = '{0:032b}'.format(index).encode()
        pack_field = packet_indicator.encode()
        total = sequence_number + pack_field + d
        check_sum = checksum(total)
        check_sum = '{0:016b}'.format(check_sum).encode()
        segment_list.append(sequence_number + check_sum + pack_field + d)
        index += 1
    return segment_list
