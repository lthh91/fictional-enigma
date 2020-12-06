import socket
import threading
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def receive_message(s, privkey):
    while True:
        msg = s.recv(2048)
        decrypted_msg = decrypt_message(privkey, msg)
        print('Received:' + decrypted_msg.decode())

def send_message(s, message):
    s.send(message)

def generate_key():
    key = RSA.generate(2048)
    pubkey = key.publickey().exportKey("PEM")
    return key, pubkey

def encrypt_message(pubkey, message):
    cipher = PKCS1_OAEP.new(pubkey)
    return cipher.encrypt(message)

def decrypt_message(privkey, encrypted_message):
    cipher = PKCS1_OAEP.new(privkey)
    return cipher.decrypt(encrypted_message)

port = 5001

s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

s.connect(('127.0.0.1', port))

try:
    key, pubkey = generate_key()
    priv_key = key.exportKey("PEM")
    s.send(priv_key)
    time.sleep(4)
    s.send(pubkey)
    msg = s.recv(2048)
    print(msg)
    friend_pubkey = RSA.importKey(msg)
    x = threading.Thread(target=receive_message, args=(s, key))
    x.start()
    while True:
        message = input("")
        encrypted_msg = encrypt_message(friend_pubkey, message.encode())
        send_message(s, encrypted_msg)
    x.join()
finally:
    s.close()
