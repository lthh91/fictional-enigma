import socket
import threading

def receive_message(c):
    while True:
        msg = c.recv(1024)
        print('Received:' + msg.decode())

def send_message(c, message):
    c.send(message.encode())

port = 5000
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

s.bind(('', port))

s.listen(1)
c, addr = s.accept()

print("Connection from: ", str(addr))

try:
    x = threading.Thread(target=receive_message, args=(c,))
    x.start()
    while True:
        message = input("")
        send_message(c, message)
    x.join()
finally:
    c.close()
