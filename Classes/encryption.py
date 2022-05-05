import random

import rsa


def generate_keys():
    (pubKey, privKey) = rsa.newkeys(1024)
    return pubKey, privKey


def encrypt_rsa(msg, key):
    return rsa.encrypt(msg.encode('ascii'), key)


def decrypt_rsa(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
    except:
        return False


def sign_sha1(msg, key):
    return rsa.sign(msg.encode('ascii'), key, 'SHA-1')


def verify_sha1(msg, signature, key):
    try:
        return rsa.verify(msg.encode('ascii'), signature, key) == 'SHA-1'
    except:
        return False


def genKey(length: int):
    key = []
    for i in range(length):
        key.append(random.randint(1, 9))
    k = ''
    for num in key:
        k += str(num)

    return k


def encrypt(msg, key):
    msg2 = []
    toencript = ''
    for i in range(3 - len(str(len(msg)))):
        toencript += '0'
    for letter in str(len(msg)):
        toencript += letter

    toencript += msg
    while len(toencript) < 256:
        toencript += chr(random.randint(ord('a'), ord('z')))

    for i in range(256):
        msg2.append(chr(ord(toencript[i]) + (i + int(key)) * int(key[i % len(key)])))

    msg3 = ''
    for letter in msg2:
        msg3 += letter

    return msg3


def decrypt(msg, key):
    msg2 = []
    lenn = ''
    for i in range(3):
        lenn += chr(ord(msg[i]) - (i + int(key)) * int(key[i % len(key)]))
    lenn = int(lenn)

    for i in range(3, 3 + lenn):
        msg2.append(chr(ord(msg[i]) - (i + int(key)) * int(key[i % len(key)])))

    msg3 = ''
    for letter in msg2:
        msg3 += letter
    return msg3
