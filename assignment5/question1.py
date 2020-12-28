import socket
import ssl
from pprint import pprint

hostname = 'www.facebook.com'
messagesize = 1024
context = ssl.create_default_context()


with socket.create_connection((hostname, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        message = "GET /index.html HTTP/1.1\r\nHost: %s\r\n\r\n"% hostname
        ssock.send(message.encode())
        response = ssock.recv(messagesize)  
        pprint(response)
