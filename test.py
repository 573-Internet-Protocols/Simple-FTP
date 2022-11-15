import time

from checksum import checksum

if __name__ == '__main__':
    f = open("test.txt", 'rb')
    data = f.read(500)
    print(len(data))
    print(type(data))
    sn = '{0:032b}'.format(1).encode()
    x = sn + data
    y = checksum(x)
    y = '{0:016b}'.format(y).encode()
    x = y + x
    print(x)
