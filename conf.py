import random
import math
from sha import *
import json


def euclid_algorithm(a, b, flag):
    r = [a, b]
    x = [1, 0]
    y = [0, 1]

    i = 0
    while r[i] != 0:
        if r[i + 1] != 0:

            q = (r[i] // r[i + 1])
            c = r[i] - q * r[i + 1]
            a = x[i] - q * x[i + 1]
            b = y[i] - q * y[i + 1]

            x.append(a)
            y.append(b)
            r.append(c)
            i += 1

        elif r[i + 1] == 0:
            break

    d = r[i]
    u = x[i]
    v = y[i]

    if flag is True:

        choose = input("1 - линейное представление НОД.\n2 - НОД.\n")
        if choose == "1":
            return f"{d} = {r[0]} * {u} + {r[1]} * {v}"
        elif choose == "2":
            return f"НОД{r[0], r[1]} = {d}"
        elif choose != "1" and choose != "2":
            return "Exit."

    elif flag is False:
        return [d, u, v]


def test_miller2(n):
    a = random.randint(1, n - 2)
    exp = n - 1
    while not exp & 1:
        exp >>= 1

    if pow(a, exp, n) == 1:
        return True

    while exp < n - 1:
        if pow(a, exp, n) == n - 1:
            return True
        exp <<= 1

    return False


def generation_prime(k):
    binary = []
    for i in range(k):
        bit = random.randint(0, 1)
        binary.append(bit)

    del binary[-1]
    binary.append(1)
    del binary[0]
    binary.insert(0, 1)

    p = int(''.join(str(x) for x in binary), 2)

    test = []
    for i in range(5):
        test.append(test_miller2(p))

    if test.count(True) == len(test):

        return p

    else:
        return generation_prime(k)


def func_rsa_generation(size):
    p = generation_prime(size)
    q = generation_prime(size)
    n = q * p
    func_euler = (p - 1) * (q - 1)
    e = random.randint(3, func_euler - 1)

    d = euclid_algorithm(e, func_euler, False)[1]
    while euclid_algorithm(e, func_euler, False)[0] != 1:
        e = random.randint(3, func_euler - 1)
        d = euclid_algorithm(e, func_euler, False)[1]
    while d < 0:
        d += func_euler

    coefficient = euclid_algorithm(q, p, False)[1]

    return [n, e, d, p, q, pow(d, 1, p - 1), pow(d, 1, q - 1), coefficient]


def int_to_bytes2(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_to_bytes(x):
    return x.to_bytes(math.ceil(math.log2(x) / 8), byteorder="big")


def text_to_int(text: str) -> int:
    return int.from_bytes(text.encode('utf-8'), 'big')


def text_to_bin(text):
    return ''.join(format(x, '08b') for x in bytearray(text, 'utf-8'))


def bin_to_text(text):
    temp_list = []
    var = None
    for i in range(len(text)):
        if i % 8 == 0:
            var = int(text[i:i + 8], 2)
            var = hex(var)[2:].zfill(2)
            temp_list.append(var)
    result = b''
    for i in temp_list:
        print(i)
        result += bytes.fromhex(i)
    return result.decode()
    # return bytes.fromhex(hex(int(text, 2))[2:]).decode()


def generation_q(r: int, p: int, k: int = 512, t: int = 10):
    r = bin(r)[2:]
    n_len = len(bin(p)[2:]) + k
    r_len = len(r)
    n = r + "0" * (n_len - r_len)
    n = int(n, 2)
    nkp = n + (p - n % p)
    count = 0
    for i in bin(nkp)[2:][r_len:]:
        if i == "0":
            count += 1
        else:
            break
    ch = 0
    q = nkp // p
    if q % 2 == 0:
        ch = 1
    flag = True
    while flag:
        check = 0
        q = nkp // p
        for i in range(1, t + 1):
            if not test_miller2(q):
                check = 1
                if ch == 0:
                    nkp = n + (p - n % p) + (p * 2 * random.randint(1, int("1" * (count - 3), 2)))
                else:
                    nkp = n + (p - n % p) + (p * (2 * random.randint(1, int("1" * (count - 3), 2)) + 1))
                if bin(nkp)[2:][: r_len] != r:
                    return -1
                break
        if check == 0:
            flag = False
    return q


def func_rsa_generation_backdoor(size: int = 512):
    '''s = '1' + ''.join([str(random.randint(0, 1)) for _ in range(255-2)]) + '1'
    p = int(sha_512(s), 16)
    while test_miller2(p) is False:
        s = '1' + ''.join([str(random.randint(0, 1)) for _ in range(255 - 2)]) + '1'
        p = int(sha_512(s), 16)'''

    s = '101011100100001110110000000011001110010011001010011100010011100011101101000100101101000010111111000100101010000111000011011100000100001001011101111000110111101000001100100010010010101101000011111101101001000110010110111101110110111010111010001101110111101'
    p = 166184920843844662821632920626102530303421347967623306476894956528048995256713580240171815126894258878003133298997044534559525478400111005034980007615431

    _key_dev_ = json.load(open('file_key_dev.json'))
    n_dev = _key_dev_['n']
    e_dev = _key_dev_['e']

    r = pow(int(s, 2), e_dev, n_dev)
    q = generation_q(r, p, 512)

    n = q * p

    func_euler = (p - 1) * (q - 1)
    e = random.randint(3, func_euler - 1)

    d = euclid_algorithm(e, func_euler, False)[1]
    while euclid_algorithm(e, func_euler, False)[0] != 1:
        e = random.randint(3, func_euler - 1)
        d = euclid_algorithm(e, func_euler, False)[1]
    while d < 0:
        d += func_euler

    coefficient = euclid_algorithm(q, p, False)[1]

    return [n, e, d, p, q, pow(d, 1, p - 1), pow(d, 1, q - 1), coefficient]

