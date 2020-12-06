import socket
import threading

def receive_message(c_from, c_to):
    while True:
        msg = c_from.recv(1024)
        print('Received:' + msg.decode())
        c_to.send(msg)

port = 5001
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)

s.bind(('', port))

s.listen(2)
c1, addr = s.accept()
print("Connection from: ", str(addr))

c2, addr = s.accept()
print("Connection from: ", str(addr))

try:
    x1 = threading.Thread(target=receive_message, args=(c1, c2, ))
    x2 = threading.Thread(target=receive_message, args=(c2, c1, ))
    x1.start()
    x2.start()
except KeyboardInterrupt:
    s.close()
    c1.close()
    c2.close()
