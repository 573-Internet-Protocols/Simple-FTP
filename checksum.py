#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def carry_around_add(a, b):
    c = a + b
    return (c & 0xffff) + (c >> 16)


def checksum(msg):
    s = 0
    for i in range(0, len(msg), 2):
        if i + 1 < len(msg):
            w = (msg[i] << 8) + (msg[i + 1])
        else:
            w = (msg[i] << 8)
        s = carry_around_add(s, w)
    return ~s & 0xffff
