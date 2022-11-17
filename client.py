#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import time
from collections import deque

from checksum import checksum

packet_indicator = '0101010101010101'
last_indicator = '1111111111111111'
time_out = 0.4


def client(server_host_name, server_port, file_name, n, mss):
    start_time = time.time()
    server_port = 7735
    cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    f = open(file_name, 'rb')
    data = f.read()
    f.close()
    size = mss
    data_list = [data[i:i + size] for i in range(0, len(data), size)]

    segment_list = get_all_segments(data_list)
    window = deque()
    timers = deque()

    index = 0
    cs.settimeout(0.04)
    received_last_ack = False

    while not received_last_ack:
        while len(window) < n and index < len(segment_list):
            window.append(index)
            timers.append(time.time())
            cs.sendto(segment_list[index], (server_host_name, server_port))
            index += 1

        try:
            ack = cs.recvfrom(2048)
            cs.settimeout(0.04)
            if ack:
                ack_sequence_number = ack[0][0:32]
                ack_int = int(ack_sequence_number, 2)
                # print('Received ACK: ', ack_int, 'window[0]: ', window[0])
                while len(window) > 0 and ack_int >= window[0] + 1:
                    window.popleft()
                    timers.popleft()
                    if ack_int == len(segment_list):
                        received_last_ack = True

        except socket.timeout:
            if time.time() - timers[0] > time_out:
                print('Timeout, sequence number = ', window[0])
                length = len(window)
                start = index - length
                window.clear()
                timers.clear()
                for i in range(start, index):
                    cs.sendto(segment_list[i], (server_host_name, server_port))
                    window.append(i)
                    timers.append(time.time())
    cs.close()
    end_time = time.time()
    print('Time used: ', end_time - start_time)
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

    sequence_number = '{0:032b}'.format(index).encode()
    pack_field = last_indicator.encode()
    total = sequence_number + pack_field + b''
    check_sum = checksum(total)
    check_sum = '{0:016b}'.format(check_sum).encode()
    segment_list.append(sequence_number + check_sum + pack_field + b'')
    return segment_list
