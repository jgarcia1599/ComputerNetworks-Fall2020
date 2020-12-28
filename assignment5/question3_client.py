import socket, ssl
from pprint import pprint

hostname = 'localhost'
messagesize = 1024
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname=False
context.verify_mode=ssl.CERT_NONE

with socket.create_connection((hostname, 8000)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        message = "Hello"
        ssock.send(message.encode())
        response = ssock.recv(messagesize)  
        pprint(response)

