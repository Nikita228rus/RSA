import json
import random
import math
from sha import *
import time


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_to_bytes2(x):
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


def rsa_dec_dev(encrypto_content, d, n, size_key=512):
    block = int(size_key / 2)

    c = [encrypto_content[x:x + block] for x in range(0, len(encrypto_content), block)]

    m = [None] * len(c)
    for i in range(len(c)):
        m[i] = int_to_bytes(pow(int(c[i], 16), d, n))

    temp_var = m[0][-1]

    for i in range(len(m) - 1):
        m[i] = m[i][:len(m[i]) - 1]

    for i in range(temp_var):
        m[-1] = m[-1][:len(m[-1]) - 1]
    result = b''.join(m).decode('utf-8')

    return result


def rsa_enc_dev(message, e, n, size_key=512):
    bytes_message = message.encode('utf-8')
    k = int(((size_key / 2) - 8) / 8)
    k2 = int(((size_key / 2) - 16) / 8)

    blocks_message = [bytes_message[x:x + k2] for x in range(0, len(bytes_message), k2)]

    if len(blocks_message[-1]) != k:
        l_var = len(blocks_message[-1])
        temp_var = (k - l_var) % k

        bytes_temp_var = int_to_bytes(temp_var)
        for i in range(temp_var):
            blocks_message[-1] = blocks_message[-1] + bytes_temp_var

        for i in range(len(blocks_message) - 1):
            blocks_message[i] = blocks_message[i] + bytes_temp_var

    for i in range(len(blocks_message)):
        blocks_message[i] = pow(int.from_bytes(blocks_message[i], 'big'), e, n)

    encrypted_content = ''
    for i in blocks_message:
        encrypted_content = encrypted_content + hex(i)[2:].zfill((k + 1) * 8)

    return encrypted_content


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


def generation_prime_determinate_size_3(k, s=''):

    padding = list(s)

    if s == '':
        binary = [1] + [random.randint(0, 1) for _ in range(k - 2)] + [1]

    elif s[0] == '0':
        binary = [1] + [int(i) for i in padding] + [random.randint(0, 1) for _ in range(k - 2 - len(s))] + [1]

    elif s[0] == '1':
        binary = [1] + [random.randint(0, 1) for _ in range(k - 2 - len(s))] + [int(i) for i in padding] + [1]

    p = int(''.join(str(x) for x in binary), 2)

    test = []
    for i in range(5):
        test.append(test_miller2(p))

    if test.count(True) == len(test):

        return p

    else:
        return generation_prime_determinate_size_3(k, s)


def iteration_q(p, r, fix=10, size_q=512):

    r_check = int(r[:fix], 2)
    print(r_check)

    q = generation_prime(size_q)
    n = p * q
    n_bin = bin(n)[2:]
    n_check = int(n_bin[:fix], 2)

    one_pad = ''
    zero_pad = ''

    while (n_check != r_check) and (len(n_bin) != size_q * 2): #
    #while n_check != r_check:

        if len(n_bin) != 1024 or n_check < r_check:
            one_pad = one_pad + '1'
            q = generation_prime_determinate_size_3(size_q, one_pad)
            n = p * q
            n_bin = bin(n)[2:]
            n_check = int(n_bin[:fix], 2)
            print(n_check)

        elif n_check > r_check:
            zero_pad = zero_pad + '0'
            q = generation_prime_determinate_size_3(size_q, zero_pad)
            n = p * q
            n_bin = bin(n)[2:]
            n_check = int(n_bin[:fix], 2)
            print(n_check)


    return q, n


def generation_q_crack(k, r, p):
    p_len = len(bin(p)[2:])
    n_len = p_len + k
    r_len = len(r)
    n = int(r + '0' * (n_len - r_len), 2)

    n_kp = n + (p - n % p)
    size_pk = 0
    for i in bin(n_kp)[2:][r_len:]:
        if i == "0":
            size_pk += 1
        else:
            break

    ch = 0
    q = n_kp // p
    if q % 2 == 0:
        ch = 1

    flag = True
    while flag:
        check = 0
        q = n_kp // p

        if not test_miller2(q):
            check = 1

            if ch == 0:
                n_kp = n + (p - n % p) + (p * 2 * random.randint(1, int("1" * (size_pk - 3), 2)))
            else:
                n_kp = n + (p - n % p) + (p * (2 * random.randint(1, int("1" * (size_pk - 3), 2)) + 1))

            if bin(n_kp)[2:][:r_len] != r:
                raise Exception()

        if check == 0:
            flag = False
    return q


def func_rsa_generation_backdoor(size):

    # generation s and p
    '''s = ''.join(['1'] + [str(random.randint(0, 1)) for _ in range(255 - 1)])
    p = int(sha_512(s), 16)
    while not(test_miller2(p)):
        s = ''.join(['1'] + [str(random.randint(0, 1)) for _ in range(255 - 1)])
        p = int(sha_512(s), 16)
    s = int(s, 2)'''
    # ----------------------

    p = 0x767e5f5b9cf75b8b973c7f98a1e9eb448d1ca375555c860aa61a9d9bb24b80769e2d747b18b90382f81e2714b1d3a1021ec50b565bee43cd577b8bdaa94a8739
    s = 35998657529196686069166308022526489059700881121852831859588034883108227626999

    dev_key = json.load(open('file_key_dev.json'))
    e_dev = dev_key['e']
    n_dev = dev_key['n']
    r = pow(s, e_dev, n_dev)    # +- 256
    q = generation_q_crack(512, bin(r)[2:], p)
    n = q * p
    # -----------------------
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







