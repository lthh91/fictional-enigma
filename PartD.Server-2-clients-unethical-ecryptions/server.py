import socket
import threading
from queue import Queue
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def receive_message(c_from, c_to, from_q, to_q):
    while True:
        msg = c_from.recv(2048)
        try:
            decoded_msg = msg.decode()
            if ('PRIVATE KEY' in decoded_msg):
                from_q.put(msg)
                continue
        except UnicodeDecodeError as e:
            print("Received Something but can't decode")
            print(msg)
            try:
                key_c_to = to_q.get()
                decrypted_msg = decrypt_message(key_c_to, msg)
                print("Decrypted Msg: {}".format(decrypted_msg.decode()))
            except Exception:
                pass
        c_to.send(msg)

def decrypt_message(key_content, encrypted_message):
    key = RSA.importKey(key_content)
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(encrypted_message)

port = 5001
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

s.bind(('', port))

s.listen(2)
c1, addr = s.accept()
print("Connection from: ", str(addr))

c2, addr = s.accept()
print("Connection from: ", str(addr))

q_c1 = Queue()
q_c2 = Queue()

try:
    x1 = threading.Thread(target=receive_message, args=(c1, c2, q_c1, q_c2))
    x2 = threading.Thread(target=receive_message, args=(c2, c1, q_c2, q_c1))
    x1.start()
    x2.start()
except KeyboardInterrupt:
    x1.join()
    x2.join()
    c1.close()
    c2.close()
