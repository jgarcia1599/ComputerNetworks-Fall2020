
import socket
import sys
import random

server_port= 8000
# Create a datagram socket for the client
udp_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#Diffie–Hellman_key_exchange
g=5
p=23
b = random.randint(0,10)
B = (g**b) % p

#Debugging 
# print(f'Server chooses the following b:{b}')
# print(f'Server sends the following B: {B}')

# Create message to send to the server
message_to_server=f"{B}"

# Send B to the server
udp_client.sendto(message_to_server.encode(),('',server_port))

#  Debugging
# print("sent: " + message_to_server)

# TODO: Receive A from the server
message_from_server = udp_client.recvfrom(1024)

#Debugging
# print(message_from_server[0])

# Computing secret message Diffie–Hellman_key_exchange
A = int(message_from_server[0].decode())
s = (A**b)%p

print("Our Secret Key: ",s)

# TODO: Close any sockets that are open
udp_client.close()