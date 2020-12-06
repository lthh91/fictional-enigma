import socket
import threading

def receive_message(s):
    while True:
        msg = s.recv(1024)
        print('Received:' + msg.decode())

def send_message(s, message):
    s.send(message.encode())


port = 5000

s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

s.connect(('127.0.0.1', port))

try:
    x = threading.Thread(target=receive_message, args=(s,))
    x.start()
    while True:
        message = input("")
        send_message(s, message)
    x.join()
finally:
    s.close()
