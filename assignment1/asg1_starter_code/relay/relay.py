import sys
# TODO: import socket libraries
import socket



NUM_TRANSMISSIONS=200
if (len(sys.argv) < 2):
  print("Usage: python3 " + sys.argv[0] + " relay_port")
  sys.exit(1)
assert(len(sys.argv) == 2)
relay_port=int(sys.argv[1])

# TODO: Create a relay socket to listen on relay_port for new connections
relay_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  

# TODO: Bind the relay's socket to relay_port
relay_socket.bind(('',relay_port))
print('Running relay server on port: ',relay_port)

# TODO: Put relay's socket in LISTEN mode
relay_socket.listen()

# TODO: Accept a connection first from sender.py (accept1)

sender_socket,sender_address = relay_socket.accept()
# TODO: Then, accept a connection from receiver.py (accept2)
receiver_socket,receiver_address = relay_socket.accept()

# Repeat NUM_TRANSMISSIONS times
for i in range(NUM_TRANSMISSIONS):
  # TODO: Receive data from sender socket (the return value of accept1)
  # Be careful with the length of data you receive
  sender_data = sender_socket.recv(201)
  string_to_parse = sender_data.decode()

  # TODO: Check for any bad words and replace them with the good words
  # Replace 'virus' with 'groot'
  string_to_parse = string_to_parse.replace('virus','groot')
  # Replace 'worm' with 'hulk'
  string_to_parse = string_to_parse.replace('worm','hulk')
  # Replace 'malware' with 'ironman'
  string_to_parse = string_to_parse.replace('malware','ironman')

  # TODO: and forward the new string to the receiver socket (the return value of accept2)
  receiver_socket.sendall(string_to_parse.encode())


  # TODO: print data that was relayed
  print('Relayed: ',string_to_parse)
  print('')

# TODO: Close all open sockets
sender_socket.close()
receiver_socket.close()
relay_socket.close()

# Resources to replace string https://www.tutorialspoint.com/python/string_replace.htm
# General Resources :
# geeks for geeks
# stack overflow for syntax questions
# class demo on sockets
