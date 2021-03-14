import math


def truncated_binary(x, n):  # it is taken from https://en.wikipedia.org/wiki/Truncated_binary_encoding
    k = 0
    t = n
    while t > 1:
        k += 1
        t >>= 1
    u = (1 << (k + 1)) - n
    if x < u:
        return binary(x, k)
    else:
        return binary(x + u, k + 1)


def binary(x, leno):  # it is taken from https://en.wikipedia.org/wiki/Truncated_binary_encoding
    s = ""
    while x != 0:
        if x % 2 == 0:
            s = '0' + s;
        else:
            s = '1' + s
        x >>= 1
    while len(s) < leno:
        s = '0' + s
    return s


def str_to_bin(string):  # it turns string into binary as an int
    form_bin = 0
    for i in range(len(string)):
        if string[i] == '1':
            form_bin |= (1 << len(string) - 1 - i)
    return form_bin


def golomb_encoding(x, b):  # it is the golomb encoding part
    q = math.floor((x - 1) / b)
    unary = 0
    for i in range(1, q + 1):
        unary |= (1 << i)

    r = x - q * b - 1
    r_result = truncated_binary(r, b)

    form_bin = str_to_bin(r_result)

    result = (1 << (len(bin(unary)[2:])) + len(r_result)) | (unary << len(r_result)) | form_bin
    # it is the concatenation between unary part and truncated binary part. And, I also added 1 as an MSB since
    # in Python, it holds value, 0b001 as 0b1. To solve this, I store this value, 0b001 as 0b1001
    return result
