#TODO: import socket library
import socket
import sys
NUM_TRANSMISSIONS=10
if(len(sys.argv) < 2):
  print("Usage: python3 " + sys.argv[0] + " server_port")
  sys.exit(1)
assert(len(sys.argv) == 2)
server_port = int(sys.argv[1])

# Helper function adapted from: https://www.geeksforgeeks.org/python-program-to-check-whether-a-number-is-prime-or-not/
def isPrime(num):
# Python program to check if  
# given number is prime or not 

  # If given number is greater than 1 
  if num > 1:    
    # Iterate from 2 to n / 2  
    for i in range(2, num): 
        # If num is divisible by any number between  
        # 2 and n / 2, it is not prime  
        if (num % i) == 0: 
            return 'no'
            break
    else: 
        return 'yes'
    
  else: 
    return 'no'

# TODO: Create a socket for the server
udp_server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# TODO: Bind it to server_port 
udp_server.bind(('',server_port))
print (" RPC Server listening for socket connections on: ",server_port)
# Repeat NUM_TRANSMISSIONS times
for i in range(NUM_TRANSMISSIONS):
  # TODO: Receive RPC request from client
  data = udp_server.recvfrom(1024)

  client_message = data[0]

  client_address = data[1]

  # TODO: Turn byte array that you received from client into a string variable called rpc_data
  rpc_data = client_message.decode()

  # TODO: Parse rpc_data to get the argument to the RPC.
  # Remember that the RPC request string is of the form prime(NUMBER)
  number_from_rpc = int(rpc_data[6:-1])

  # TODO: Print out the argument for debugging
  print("Argument is: ",number_from_rpc)


  # TODO: Compute if the number is prime (return a 'yes' or a 'no' string)
  is_prime = isPrime(number_from_rpc)

  # TODO: Send the result of primality check back to the client who sent the RPC request
  udp_server.sendto(is_prime.encode(),client_address)

# TODO: Close server's socket
udp_server.close()

# resources : https://pythontic.com/modules/socket/udp-client-server-example
# General Resources :
# geeks for geeks
# stack overflow for syntax questions
# class demo on sockets




