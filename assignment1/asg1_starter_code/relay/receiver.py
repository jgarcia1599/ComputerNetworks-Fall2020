import sys
import os
import random
import string
#TODO: import socket libraries
import socket

NUM_TRANSMISSIONS=200
if (len(sys.argv) < 2):
  print("Usage: python3 " + sys.argv[0] + " relay_port")
  sys.exit(1)
assert(len(sys.argv) == 2)
relay_port=int(sys.argv[1])

# TODO: Create a socket for the receiver
receiver_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
print('Receiver socket running on: ',relay_port)

# TODO: Connect this socket to the relay at relay_port
receiver_socket.connect(('',relay_port))

# Iterate NUM_TRANSMISSIONS times
for i in range(NUM_TRANSMISSIONS):
  # TODO: Receive any data relayed from the relay (i.e., any data sent by the sender to the relay)
  received_data = receiver_socket.recv(201)

  # TODO: Print received data
  print('Received:',received_data.decode())
# TODO: Close any open sockets
receiver_socket.close()

# Resources :
# geeks for geeks
# stack overflow for syntax questions
# class demo on sockets
