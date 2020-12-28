# TODO: import socket library
import socket
import sys
import random
NUM_TRANSMISSIONS=10
if (len(sys.argv) < 2):
  print("Usage: python3 " + sys.argv[0] + " server_port")
  sys.exit(1)
assert(len(sys.argv) == 2)
server_port=int(sys.argv[1])

# TODO: Create a datagram socket for the client
udp_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# Repeat NUM_TRANSMISSIONS times
for i in range(NUM_TRANSMISSIONS):
  # Create an RPC request to compute if a number is prime
  rpc_data="prime(" + str(random.randint(0, 100)) + ")"

  # TODO: Send RPC request (i.e., rpc_data) to the server
  udp_client.sendto(rpc_data.encode(),('',server_port))

  # Print debugging information
  print("sent: " + rpc_data)

  # TODO: Receive result back from the server into the variable result_data
  message_from_server = udp_client.recvfrom(1024)

  # TODO: Display it in the format "prime: yes" or "prime: no"
  print("prime: ",message_from_server[0].decode())
  print("")

# TODO: Close any sockets that are open
udp_client.close()

# resources : https://pythontic.com/modules/socket/udp-client-server-example
# General Resources :
# geeks for geeks
# stack overflow for syntax questions
# class demo on sockets