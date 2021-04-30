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


def desencriptar(dire, key, iv, dirout):
    archivo = open(dire, "rb")
    tam = os.path.getsize(dire)
    print(tam)
    print(len(archivo.read()))
    encriptador = AES.new(key, AES.MODE_CBC, iv)
    archivo_desencriptado = open(dirout, 'wb')
    while True:
        data = archivo.read(256)
        n = len(data)
        if n == 0:
            break
        decd = encriptador.decrypt(data)
        n = len(decd)
        if tam > n:
            archivo_desencriptado.write(decd)
        else:
            archivo_desencriptado.write(decd[:tam])
        tam -= n
    archivo.close()
    archivo_desencriptado.close()

    
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
HOST = '127.0.0.1'
PORT = 65432
server_address = (HOST, PORT)
#print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
sock.listen(1)


while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    public_key, secret_key = generate_keypair()
    amount_expected = 1088
    amount_received = 0

    try:
        #FASE1
        print('client connected:', client_address)
        connection.sendall(public_key)
        print('pk enviada')
        print(len(public_key))
        ciphertext = connection.recv(1088)
        print('ct recibido')
        plaintext_recovered = decrypt(secret_key, ciphertext)
        print('pt enviado')   
        connection.sendall(plaintext_recovered)
        salt = b'1234567891123456'
        key = scrypt(plaintext_recovered, salt, 16, N=2**14, r=8, p=1)
        #FIN_FASE1
        #FASE2
        public_key_sign, secret_key_sign = generate_keypair()
        connection.sendall(public_key_sign)
        #FINFASE2

        '''
        while True:
            ciphertext = connection.recv(1088)
            amount_received += len(ciphertext)
            if not ciphertext:
                plaintext_recovered = decrypt(secret_key, ciphertext)
                connection.sendall(plaintext_recovered)
                break
            elif amount_received > amount_expected:
                sys.exit('Existe un problema con la longitud del ct')
                break

        print('ct recibido')        
        '''
        
    finally:
        connection.close()
