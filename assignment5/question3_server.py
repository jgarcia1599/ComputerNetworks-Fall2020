import socket
import ssl
from pprint import pprint

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain('cert.pem')

bindsocket = socket.socket()
bindsocket.bind(('localhost', 8000))
bindsocket.listen(5)

while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = context.wrap_socket(newsocket, server_side=True)
    try:
        data = connstream.recv(1024)
        print(data)
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
