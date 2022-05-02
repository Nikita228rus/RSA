from conf import *
import random
import json
import timeit
import sys


# s = 'affffffffffafsfaaaaaaaaaaasfwagsgфафаhc♠♥♥☻♣○☻♦U♣♠7+♣♥♣+☺☺♂☺i♣affffffffffafsfaaaaaaaaaaasfwagsgфафаhc♠♥♥☻♣○☻♦U♣♠7+♣♥♣+☺☺♂☺i♣affffffffffafsfaaaaaaaaaaasfwagsgфафаhc♠♥♥☻♣○☻♦U♣♠7+♣♥♣+☺☺♂☺i♣affffffffffafsfaaaaaaaaaaasfwagsgфафаhc♠♥♥☻♣○☻♦U♣♠7+♣♥♣+☺☺♂☺i♣'


def menu():
    choose = input('1 - encryption\n2 - decryption\n3 - exit\n>>>\t')


    if choose == '1':
        size_key = int(input('size key: '))
        '''choose_size_key = int(input('size key:\n1 - 512\n2 - 1024\n3 - 2048\n>>>\t'))
        if choose_size_key == '1':
            size_key = 512
        elif choose_size_key == '2':
            size_key = 1024
        elif choose_size_key == '3':
            size_key = 2048'''

        choose = input('1 - read file\n2 - input keyboard\n>>>\t')
        if choose == '1':
            mess = open('input.txt', 'r', encoding='utf-8').read()
        elif choose == '2':
            mess = input('Input message:\t')

        encrypt = rsa_encryption(mess, size_key)
        open('output.txt', 'w', encoding='utf-8').write(encrypt)

    elif choose == '2':

        decrypt = rsa_decryption()
        open('output.txt', 'w', encoding='utf-8').write(decrypt)

    elif choose == '3':
        exit()
    menu()


def rsa_decryption():
    _message_struc_ = json.load(open('file_PKCS7.json'))
    _private_key_ = json.load(open('file_PKCS12.json'))
    _public_key_ = json.load(open('file_PKCS8.json'))
    c = _message_struc_["EncryptedContentInfo"]["OPTIONAL"]
    d = _private_key_['privateExponent']
    n = _public_key_['SubjectPublicKeyInfo']['N']
    m = [None] * len(c)
    for i in range(len(c)):
        m[i] = int_to_bytes(pow(c[i], d, n))

    result = b''.join(m).decode('utf-8')
    if _message_struc_['dump'] is None:
        size = 0
    else:
        size = _message_struc_['dump']

    print(result)
    return result[:len(result) - size]


def rsa_encryption(message, size_key):
    bytes_message = message.encode()

    _data_ = {'dump': None,
              'EncryptedContentInfo': {'ContentType': 'text',
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
                     'coefficient': None}

    k = int(size_key / 16)
    '''choose_k = input('size block:\n1 - 512\n2 - 1024\n3 - 2048\n>>>\t')
    if choose_k == '1':
        k = int(512 / 8)
    elif choose_k == '2':
        k = int(1024 / 8)
    elif choose_k == '3':
        k = int(2048 / 8)
    else:
        print('Try again...')
        return rsa_encryption(message)'''



    blocks_message = [bytes_message[x:x + k] for x in range(0, len(bytes_message), k)]

    if len(blocks_message[-1]) != k:
        l = len(blocks_message[-1])
        temp_var = (k - l) % k
        _data_['dump'] = temp_var
        bytes_temp_var = int_to_bytes(temp_var)
        for i in range(temp_var):
            blocks_message[-1] = blocks_message[-1] + bytes_temp_var

    key = func_rsa_generation(size_key)

    _public_key_['SubjectPublicKeyInfo']['publicExponent'] = key[1]
    _public_key_['SubjectPublicKeyInfo']['N'] = key[0]
    _private_key_['privateExponent'] = key[2]
    _private_key_['prime1'] = key[3]
    _private_key_['prime2'] = key[4]
    _private_key_['exponent1'] = key[5]
    _private_key_['exponent2'] = key[6]
    _private_key_['coefficient'] = key[7]

    for i in range(len(blocks_message)):
        blocks_message[i] = pow(int.from_bytes(blocks_message[i], 'big'), key[1], key[0])

    _data_['EncryptedContentInfo']['OPTIONAL'] = blocks_message
    encryptedContent = ''
    for i in blocks_message:
        encryptedContent = encryptedContent + hex(i)[2:]
    _data_['EncryptedContentInfo']['encryptedContent'] = encryptedContent

    json.dump(_data_, open('file_PKCS7.json', 'w+'))
    json.dump(_public_key_, open('file_PKCS8.json', 'w+'))
    json.dump(_private_key_, open('file_PKCS12.json', 'w+'))

    return _data_['EncryptedContentInfo']['encryptedContent']


#menu()


# func_rsa(s)
# print(timeit.timeit('func()', number=10, globals=globals()))