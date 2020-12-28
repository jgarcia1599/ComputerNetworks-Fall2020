#import socket library
import socket
import sys
import random

server_port = 8000

#Create a socket for the server
udp_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# Bind it to server_port 
udp_server.bind(('',server_port))

#Diffie–Hellman_key_exchange
g=5
p=23
a = random.randint(0,10)
A = (g**a) % p

#Debugging
# print(f'Server chooses the following a:{a}')
# print(f'Server sends the following A: {A}')

# Receive B  from client
data = udp_server.recvfrom(1024)
client_message = data[0]

# Computing secret message Diffie–Hellman_key_exchange
B = int(client_message.decode())
s = (B**a)%p
# Send A to Client
message_to_client = f"{A}"
udp_server.sendto(message_to_client.encode(),client_address)

print(f"Server: Our Secret key is {s}")
#  Close server's socket
udp_server.close()

