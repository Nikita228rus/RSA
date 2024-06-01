import random

def generation_prime_determinate_size(k, flag=['b', []]):
    binary = []
    flag_start = flag.copy()
    for i in range(k):
        bit = random.randint(0, 1)
        binary.append(bit)

    del binary[-1]
    binary.append(1)
    del binary[0]
    binary.insert(0, 1)

    if flag[0] == 'b' and len(flag[1]) == 0:
        for i in range(1, len(binary)):
            if binary[i] == 1:
                binary[i] = 0
                flag[1].append(i)
                break

    elif flag[0] == 's' and len(flag[1]) == 0:
        for i in range(len(binary) - 2, 1, -1):
            if binary[i] == 0:
                binary[i] = 1
                flag[1].append(i)
                break

    elif flag[0] == 'b' and len(flag[1]) != 0:
        for i in flag[1]:
            binary[i] = 0
        for i in range(flag[1][-1], len(binary)):
            if binary[i] == 1:
                binary[i] = 0
                flag[1].append(i)

    elif flag[0] == 's' and len(flag[1]) != 0:
        for i in flag[1]:
            binary[i] = 1
        for i in range(flag[1][-1], 1, -1):
            if binary[i] == 0:
                binary[i] = 1
                flag[1].append(i)
                break

    p = int(''.join(str(x) for x in binary), 2)

    test = []
    for i in range(5):
        test.append(test_miller2(p))

    if test.count(True) == len(test):

        return p, flag

    else:
        return generation_prime_determinate_size(k, flag_start)


def generation_prime_determinate_size_2(k, flag=['b', []]):
    while True:
        binary = []
        flag_start = flag.copy()
        for i in range(k):
            bit = random.randint(0, 1)
            binary.append(bit)

        del binary[-1]
        binary.append(1)
        del binary[0]
        binary.insert(0, 1)

        if flag[0] == 'b' and len(flag[1]) == 0:
            for i in range(1, len(binary)):
                if binary[i] == 1:
                    binary[i] = 0
                    flag[1].append(i)
                    break

        elif flag[0] == 's' and len(flag[1]) == 0:
            for i in range(len(binary) - 2, 1, -1):
                if binary[i] == 0:
                    binary[i] = 1
                    flag[1].append(i)
                    break

        elif flag[0] == 'b' and len(flag[1]) != 0:
            for i in flag[1]:
                binary[i] = 0
            for i in range(flag[1][-1], len(binary)):
                if binary[i] == 1:
                    binary[i] = 0
                    flag[1].append(i)

        elif flag[0] == 's' and len(flag[1]) != 0:
            for i in flag[1]:
                binary[i] = 1
            for i in range(flag[1][-1], 1, -1):
                if binary[i] == 0:
                    binary[i] = 1
                    flag[1].append(i)
                    break

        p = int(''.join(str(x) for x in binary), 2)

        test = []
        for i in range(5):
            test.append(test_miller2(p))

        if test.count(True) == len(test):
            return p, flag

        flag = flag_start


# print(generation_prime_determinate_size_2(10, flag_left))

'''
601
1021 ['s', [7, 5, 4, 2]]
'''


def fast_gen_q(p, r, fix=10):
    n_fix = r[:fix]

    while True:
        num_bytes = 1024 // 8
        random_bytes = bytes([random.randint(0, 255) for _ in range(num_bytes)])
        random_bin = bin(int.from_bytes(random_bytes, byteorder='big'))[2:]
        sub = 1024 - len(random_bin)
        n = n_fix + random_bin[10 - sub:]
        n = n[:1023] + '1'

        ost = int(n, 2) % p
        print(ost)
        if ost == 0:
            return int(n, 2) / p


# fast_gen_q(p, r)


def generation_prime_determinate_size_3(k, s):
    padding = list(s)
    if s[0] == '0':
        binary = [1] + [int(i) for i in padding] + [random.randint(0, 1) for _ in range(k - 2 - len(s))] + [1]

    elif s[0] == '1':
        s = list(s)
        binary = [1] + [random.randint(0, 1) for _ in range(k - 2 - len(s))] + [int(i) for i in padding] + [1]

    p = int(''.join(str(x) for x in binary), 2)

    test = []
    for i in range(5):
        test.append(test_miller2(p))

    if test.count(True) == len(test):

        return p

    else:
        print('+')
        return generation_prime_determinate_size_3(k, s)





# q = 11661278783102897489614008427675326745674795168022735022191235072764053792792311317678680268881996261313377322581815063820365573976910652328048141865141223


q = 11661278783102897489614008427675326745674795168022735022191235072764053792792311317678680268881996261313377322581815063820365573976910652328048141865141223
s = '10001000101100110001101100111011110011010111111000101100001110011111010010001010010011110111001000010001001101011011010001111111101100110010111000010110110110001101011111001111011011110010100010111001100000011011111011000010111110111111110101111001110111101110101101110010000011000010100011001011100010101011011011110111001010011110100100111101110011110101111101000111100011100100111011011111000001011011000110001000000101010010010001100111111100110000001000001110100011101101011110010000011010111110000101001000'


p = int(sha_512(s), 16)

# iteration_q(p, r)

def func_for_test(k, iteration):
    start = time.time()
    for _ in range(iteration):
        binary = [1] + [random.randint(0, 1) for _ in range(k - 2)] + [1]
    end = time.time()

    print(f'{end - start} - time func_new')

    start = time.time()
    for _ in range(iteration):
        binary = []
        for i in range(k):
            bit = random.randint(0, 1)
            binary.append(bit)

        del binary[-1]
        binary.append(1)
        del binary[0]
        binary.insert(0, 1)
    end = time.time()

    print(f'{end - start} - time func_old')


def test_func(k, *args):
    if len(args) == 0:
        binary = [1] + [random.randint(0, 1) for _ in range(k - 2)] + [1]

    if len(args) == 1:

        s = args[0]
        padding = list(s)
        if s[0] == '0':
            binary = [1] + [int(i) for i in padding] + [random.randint(0, 1) for _ in range(k - 2 - len(s))] + [1]

        elif s[0] == '1':
            binary = [1] + [random.randint(0, 1) for _ in range(k - 2 - len(s))] + [int(i) for i in padding] + [1]

    elif len(args) == 2:
        s_0 = args[0]
        s_1 = args[1]
        padding_0 = list(s_0)
        padding_1 = list(s_1)
        binary = [1] + [int(i) for i in padding_0] + [random.randint(0, 1) for _ in
                                                      range(k - 2 - len(s_0) - len(s_1))] + [int(i) for i in
                                                                                             padding_1] + [1]

    p = int(''.join(str(x) for x in binary), 2)

    test = []
    for i in range(5):
        test.append(test_miller2(p))

    if test.count(True) == len(test):

        return p

    else:
        return test_func(k, *args)


def iteration_q(p, r, fix=10, size_q=512):

    r_check = int(r[:fix], 2)
    print(r_check)

    q = generation_prime(size_q)
    n = p * q
    n_bin = bin(n)[2:]
    n_check = int(n_bin[:fix], 2)

    one_pad = ''
    zero_pad = ''

    #while (n_check != r_check) and (len(n_bin) != size_q * 2):
    while n_check != r_check:

        #if len(n_bin) != 1024 or n_check < r_check:
        if n_check < r_check:
            one_pad = one_pad + '1'
            q = test_func(size_q, zero_pad, one_pad)
            n = p * q
            n_bin = bin(n)[2:]
            n_check = int(n_bin[:fix], 2)
            print(one_pad)
            print(n_check)

        elif n_check > r_check:
            zero_pad = zero_pad + '0'
            q = test_func(size_q, zero_pad, one_pad)
            n = p * q
            n_bin = bin(n)[2:]
            n_check = int(n_bin[:fix], 2)
            print(zero_pad)
            print(n_check)

    print(r_check == n_check)
    return q, n


s = '10001000101100110001101100111011110011010111111000101100001110011111010010001010010011110111001000010001001101011011010001111111101100110010111000010110110110001101011111001111011011110010100010111001100000011011111011000010111110111111110101111001110111101110101101110010000011000010100011001011100010101011011011110111001010011110100100111101110011110101111101000111100011100100111011011111000001011011000110001000000101010010010001100111111100110000001000001110100011101101011110010000011010111110000101001000'
p = int(sha_512(s), 16)
print(p)
dev_key = json.load(open('file_key_dev.json'))
e_dev = dev_key['e']
n_dev = dev_key['n']
d_dev = dev_key['d']

# r = bin(int(rsa_enc_dev(s, e_dev, n_dev), 16))[2:]
r = bin(pow(int(s, 2), e_dev, n_dev))[2:]
print(r)
print(len(r))


#q, n = iteration_q(p, r)

def genProstPodvoh(k, r, p):
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
                print(r)
                print(bin(n_kp)[2:][:r_len])
                raise Exception()

        if check == 0:
            flag = False
    return q


k = 512
#r = bin(23031457922655198575803153635667950707288638278096423820530241257548945895226637825825568945400566402844092876208343536433938486376673822888656523104710134853685755290864543731182183607994456989805976531366730944963119556051501783159362067383018998864075651578012658496281562284521379789429684250366696205074)[2:]
p = 7899472073475512223788310525682926194089142410152097804363220701633328695526594546865540895507444131202659573448116555367689108540760120733446111655249719

q = genProstPodvoh(k, r, p)
print(test_miller2(q))
r = int(r, 2)


def genProstPodvoh(k: int, t: int, r: int, p: int):  # k - размер, t- итеарции проверки, r-E(s), p-простое
    r = bin(r)[2:]
    pl = len(bin(p)[2:])
    lenN = pl + k
    lr = len(r)
    n = r + "0" * (lenN - lr)
    n = int(n, 2)
    nKratP = n + (p - n % p)  # ---------------------------------------------------------------
    razmerPKrat = 0
    tuta = bin(nKratP)[2:][lr:]
    for i in tuta:
        if i == "0":
            razmerPKrat += 1
        else:
            break
    ch = 0
    q = nKratP // p
    if q % 2 == 0:
        ch = 1
    flag = True
    while flag:
        check = 0
        q = nKratP // p
        for i in range(1, t + 1):
            if not test_miller2(q):
                check = 1
                if ch == 0:
                    nKratP = n + (p - n % p) + (p * 2 * random.randint(1, int("1" * (razmerPKrat - 3), 2)))
                else:
                    nKratP = n + (p - n % p) + (p * (2 * random.randint(1, int("1" * (razmerPKrat - 3), 2)) + 1))
                if bin(nKratP)[2:][: lr] != r:
                    raise Exception()
                break
        if check == 0:
            flag = False
    return q


q = genProstPodvoh(512, 2, r, p)
print(test_miller2(q))