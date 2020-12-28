import sys
import os
import random
import string
# TODO: Import socket library
import socket

# Random alphanumeric string of length l
def rand_str(l):
  ret = ''
  for i in range(l):
    ret += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
  return ret

NUM_TRANSMISSIONS=10
if (len(sys.argv) < 2):
  print("Usage: python3 "  + sys.argv[0] + " server_port")
  sys.exit(1)
assert(len(sys.argv) == 2)
server_port=int(sys.argv[1])

# TODO: Create a socket for the client
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# TODO: Connect this socket to the server

host = socket.gethostname()
client_socket.connect(('',server_port))
# Transmit NUM_TRANSMISSIONS number of times
for i in range(NUM_TRANSMISSIONS):
  # TODO: Generate a random string of length 10 using rand_str function
  random_string = rand_str(10)

  # TODO: Send random string to the server
  client_socket.sendall(random_string.encode())

  # TODO: Print data for debugging
  print("Sending the following to the server: ",random_string)

  # TODO: Receive concatenated data back from server as a byte array
  received_data_from_server = client_socket.recv(1024)

  # TODO: Print out concatenated data for debugging
  print("Receiving the following from the server: ",received_data_from_server.decode())

# TODO: close socket
client_socket.close()



# Resources : 

# https://docs.python.org/2/library/socket.html#socket.socket.sendall
# https://stackoverflow.com/questions/33003498/typeerror-a-bytes-like-object-is-required-not-str
# https://stackoverflow.com/questions/22710003/python-socket-script-how-to-send-data-to-specific-client
# https://steelkiwi.com/blog/working-tcp-sockets/
# https://stackoverflow.com/questions/54016220/how-to-continuously-receive-data
# https://stackoverflow.com/questions/16130786/why-am-i-getting-the-error-connection-refused-in-python-sockets#:~:text=This%20error%20means%20that%20for,the%20computer%20running%20server%20script.&text=check%20if%20you%20can%20access,your%20OS)%20from%20the%20client

# https://www.reddit.com/r/learnpython/comments/aavi0a/connectionrefusederror_errno_111_connection/
# https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
# https://stackoverflow.com/questions/55032621/oserror-errno-57-socket-is-not-connected

