# TODO: import socket library
import socket
import sys
import random
import string

# Function to generate random strings of length l
def rand_str(l):
  ret = ''
  for i in range(l):
    ret += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
  return ret

NUM_TRANSMISSIONS=10
if (len(sys.argv) < 2):
  print("Usage: python3 " + sys.argv[0] + " server_port")
  sys.exit(1)
assert(len(sys.argv) == 2)
server_port=int(sys.argv[1])

# TODO: Create a socket for the server on localhost
tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  

# TODO: Bind it to a specific server port supplied on the command line
tcp_server.bind(('',server_port))
print ("Server listening for socket connections on: ",server_port)

# TODO: Put server's socket in LISTEN mode
tcp_server.listen()

# TODO: Call accept to wait for a connection
client_socket,client_addr = tcp_server.accept()
# Repeat NUM_TRANSMISSIONS times
for i in range(NUM_TRANSMISSIONS):
  # TODO: receive data over the socket returned by the accept() method
  # https://stackoverflow.com/questions/54016220/how-to-continuously-receive-data
  received_data = client_socket.recv(4096)

  received_data = received_data.decode()

  # TODO: print out the received data for debugging
  print ("Received data from client: ",received_data)

  # TODO: Generate a new string of length 10 using rand_str
  new_string = rand_str(10)

  print('Appended the following: ',new_string)

  # TODO: Append the string to the buffer received
  new_string = new_string +  received_data

  # TODO: Send the new string back to the client
  print("Send Data back to client:",new_string)
  print('')
  client_socket.sendall(new_string.encode())

# TODO: Close all sockets that were created
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