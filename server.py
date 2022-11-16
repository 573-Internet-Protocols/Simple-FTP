#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import socket

from checksum import checksum

random.seed(7735)

ack_indicator = '1010101010101010'
last_indicator = '1111111111111111'


def server(port, file_name, p):
    port = 7735
    ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ss.bind(('', port))

    content = b''
    next_expect_sequence_number = 0
    received_last_segment = False

    while not received_last_segment:
        data, client_address = ss.recvfrom(2048)
        if data:
            sequence_number = data[0:32]
            check_sum = data[32:48]
            pack_field = data[48:64]
            d = data[64:]
            if int(sequence_number, 2) == next_expect_sequence_number:
                new_check_sum = checksum(sequence_number + pack_field + d)
                new_check_sum = '{0:016b}'.format(new_check_sum).encode()
                if new_check_sum == check_sum:
                    r = get_random()
                    if r > p:
                        content += d
                        next_expect_sequence_number += 1
                        ack_sequence_number = next_expect_sequence_number
                        ack_sequence_number = '{0:032b}'.format(ack_sequence_number).encode()
                        all_zero = '{0:016b}'.format(0).encode()
                        ack_field = ack_indicator.encode()
                        ack = ack_sequence_number + all_zero + ack_field
                        ss.sendto(ack, client_address)
                        if pack_field == last_indicator.encode():
                            received_last_segment = True
                    else:
                        print('Packet loss, sequence number = ', int(sequence_number, 2))

    ss.close()
    f = open(file_name, 'wb')
    f.write(content)
    f.close()
    return None


def get_random():
    r = random.uniform(0, 1)
    while r == 0:
        r = random.uniform(0, 1)
    return r
