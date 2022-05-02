import random
import math


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
