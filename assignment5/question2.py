import socket
import ssl
from pprint import pprint
import sys

hostname = sys.argv[1]
context = ssl.create_default_context()

with socket.create_connection((hostname, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        pprint(ssock.getpeercert())