import socket
import sys
import os
import pqcrypto

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from secrets import compare_digest
from pqcrypto.kem.kyber768 import generate_keypair, encrypt, decrypt
from pqcrypto.sign.dilithium3 import generate_keypair, sign, verify
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes


def encriptar(dire, key, iv, dirout):
    encriptador = AES.new(key, AES.MODE_CBC, iv)
    archivo = open(dire, "rb")
    archivo_encriptado = open(dirout, "wb")
    while True:
        data = archivo.read(16)
        n = len(data)
        if n == 0:
            break
        elif n % 16 != 0:
            data += b' ' * (16 - n % 16)
        enc = encriptador.encrypt(data)
        archivo_encriptado.write(enc)
    archivo.close()
    archivo_encriptado.close()
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server
# given by the caller
server_address = ('127.0.0.1', 65432)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    #FASE1
    amount_expected = 1184
    amount_received = 0
    print('recibiendo pk')
    public_key = sock.recv(1184)
    print('pk recibida')
    ciphertext, plaintext_original = encrypt(public_key)
    sock.sendall(ciphertext)
    hash = SHA256.new()
    hash.update(ciphertext)
    ct_hash = hash.digest()
    print(ct_hash)
    print('ct enviado')
    data = sock.recv(1024)
    print(len(data))
    print(compare_digest(plaintext_original, data))
    salt = b'1234567891123456'
    key = scrypt(plaintext_original, salt, 16, N=2**14, r=8, p=1)
    #FINFASE1
    #FASE2
    public_key_sign=sock.recv(1952)
    mensaje=
    #FINFASE2


    '''
    while True:
        public_key = sock.recv(1184)
        amount_received += len(public_key)
        print("recibiendo...")
        if not public_key:
            print('pk recibida')
            ciphertext, plaintext_original = encrypt(public_key)
            sock.sendall(ciphertext)
            print('ct enviado')
            while True:
                data = sock.recv(1024)
                if not data:
                    assert compare_digest(plaintext_original, data)
                    break
            break
        elif amount_received > amount_expected:
            sys.exit('Existe un problema con la longitud de llave')
            break
          
    hash = SHA256.new()
    hash.update(ciphertext)
    ct_hash = hash.digest()
    '''

finally:
    sock.close()
