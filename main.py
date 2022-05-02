from conf import *
import json


def new_rsa_encryption(message, size_key):
    _data_ = {'EncryptedContentInfo': {'ContentType': 'text',
                                       'ContentEncryptionAlgorithmIdentifier': 'rsaEncryption',
                                       'encryptedContent': None,
                                       'OPTIONAL': None}}

    _public_key_ = {'SubjectPublicKeyInfo': {
        'publicExponent': None,
        'N': None
    }}

    _private_key_ = {'privateExponent': None,
                     'prime1': None,
                     'prime2': None,
                     'exponent1': None,
                     'exponent2': None,
                     'coefficient': None,
                     'N': None}

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

    key = func_rsa_generation(size_key)

    for i in range(len(blocks_message)):
        blocks_message[i] = pow(int.from_bytes(blocks_message[i], 'big'), key[1], key[0])

    encrypted_content = ''
    for i in blocks_message:
        encrypted_content = encrypted_content + hex(i)[2:].zfill((k + 1) * 8)

    key[0] = bin(key[0])[2:].zfill(size_key * 2)

    _public_key_['SubjectPublicKeyInfo']['publicExponent'] = key[1]
    _public_key_['SubjectPublicKeyInfo']['N'] = key[0]
    _private_key_['N'] = key[0]
    _private_key_['privateExponent'] = key[2]
    _private_key_['prime1'] = key[3]
    _private_key_['prime2'] = key[4]
    _private_key_['exponent1'] = key[5]
    _private_key_['exponent2'] = key[6]
    _private_key_['coefficient'] = key[7]
    _data_['EncryptedContentInfo']['encryptedContent'] = encrypted_content

    json.dump(_data_, open('file_PKCS7.json', 'w+'))
    json.dump(_public_key_, open('file_PKCS8.json', 'w+'))
    json.dump(_private_key_, open('file_PKCS12.json', 'w+'))

    return encrypted_content


def rsa_encryption_backdoor(message, size_key=512):
    _data_ = {'EncryptedContentInfo': {'ContentType': 'text',
                                       'ContentEncryptionAlgorithmIdentifier': 'rsaEncryption',
                                       'encryptedContent': None,
                                       'OPTIONAL': None}}

    _public_key_ = {'SubjectPublicKeyInfo': {
        'publicExponent': None,
        'N': None
    }}

    _private_key_ = {'privateExponent': None,
                     'prime1': None,
                     'prime2': None,
                     'exponent1': None,
                     'exponent2': None,
                     'coefficient': None,
                     'N': None}

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

    key = func_rsa_generation_backdoor(size_key)

    for i in range(len(blocks_message)):
        blocks_message[i] = pow(int.from_bytes(blocks_message[i], 'big'), key[1], key[0])

    encrypted_content = ''
    for i in blocks_message:
        encrypted_content = encrypted_content + hex(i)[2:].zfill((k + 1) * 8)

    key[0] = bin(key[0])[2:].zfill(size_key * 2)

    _public_key_['SubjectPublicKeyInfo']['publicExponent'] = key[1]
    _public_key_['SubjectPublicKeyInfo']['N'] = key[0]
    _private_key_['N'] = key[0]
    _private_key_['privateExponent'] = key[2]
    _private_key_['prime1'] = key[3]
    _private_key_['prime2'] = key[4]
    _private_key_['exponent1'] = key[5]
    _private_key_['exponent2'] = key[6]
    _private_key_['coefficient'] = key[7]
    _data_['EncryptedContentInfo']['encryptedContent'] = encrypted_content

    json.dump(_data_, open('file_PKCS7.json', 'w+'))
    json.dump(_public_key_, open('file_PKCS8.json', 'w+'))
    json.dump(_private_key_, open('file_PKCS12.json', 'w+'))

    return encrypted_content


def rsa_decryption():
    _message_struct_ = json.load(open('file_PKCS7.json'))
    _private_key_ = json.load(open('file_PKCS12.json'))

    text = _message_struct_["EncryptedContentInfo"]["encryptedContent"]
    d = _private_key_['privateExponent']
    n = _private_key_['N']
    block = int(len(n) / 4)
    n = int(n, 2)
    c = [text[x:x + block] for x in range(0, len(text), block)]

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


def rsa_crack():
    dev_key = json.load(open('file_key_dev.json'))
    public_key = json.load(open('file_PKCS8.json'))
    message_file = json.load(open('file_PKCS7.json'))

    # dev keys
    d_dev = dev_key['d']
    n_dev = dev_key['n']
    n_len = len(bin(n_dev)[2:])

    # public keys
    e = public_key['SubjectPublicKeyInfo']['publicExponent']
    n = public_key['SubjectPublicKeyInfo']['N']

    n_temp = n
    while n_temp[0] != '1':
        n_temp = n_temp[1:]

    message_encrypt = message_file['EncryptedContentInfo']['encryptedContent']

    secret_part = 255

    p = 225
    while not test_miller2(p):
        r = n_temp[:secret_part]
        s = bin(pow(int(r, 2), d_dev, n_dev))[2:]
        p = int(sha_512(s), 16)
        secret_part -= 1

    n_dec = int(n, 2)
    q = n_dec // p

    block = int(len(n) / 4)
    n = int(n, 2)

    func_euler = (p - 1) * (q - 1)

    d = euclid_algorithm(e, func_euler, False)[1]
    while d < 0:
        d += func_euler

    c = [message_encrypt[x:x + block] for x in range(0, len(message_encrypt), block)]

    m = [None] * len(c)
    for i in range(len(c)):
        m[i] = int_to_bytes(pow(int(c[i], 16), d, n))

    temp_var = m[0][-1]

    for i in range(len(m) - 1):
        m[i] = m[i][:len(m[i]) - 1]

    for i in range(temp_var):
        m[-1] = m[-1][:len(m[-1]) - 1]
    result = b''.join(m).decode('utf-8')

    print(result)


def menu():
    choose = input('1 - encryption\n2 - decryption\n3 - exit\n>>>\t')

    if choose == '1':
        size_key = int(input('size key: '))

        choose = input('1 - read file\n2 - input keyboard\n>>>\t')
        if choose == '1':
            mess = open('input.txt', 'r', encoding='utf-8').read()
            encrypt = new_rsa_encryption(mess, size_key)
            open('output.txt', 'w', encoding='utf-8').write(encrypt)
        elif choose == '2':
            mess = input('Input message:\t')
            encrypt = new_rsa_encryption(mess, size_key)
            open('output.txt', 'w', encoding='utf-8').write(encrypt)

    elif choose == '2':

        decrypt = rsa_decryption()
        open('output.txt', 'w', encoding='utf-8').write(decrypt)

    elif choose == '3':
        exit()
    menu()










