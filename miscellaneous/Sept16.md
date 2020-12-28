
## Sept_16


### UDP 
client
```python
from socket import *
sock_object = socket(AF_INET,SOCK_DGRAM)
sock_object.sendto(b"hello",("127.0.0.1",8000))
```

check data transfer
```
nc -l 8000 -u -> to send socket data and test
```

server
```python
from socket import *
sock_receiver = socket(AF_INET,SOCK_DGRAM)
sock_receiver.bind(("127.0.0.1",8000))
sock_receiver.recv(4096)
```

do not wait 
```python
sock_receiver.setblocking(False)
```
    
Why would we want to use a non-blocking receiver? 
Page 5 of the lecture notes



### TCP

server
```python
from socket import *
tcp_socket = socket(AF_INET,SOCK_STREAM)
tcp_server.bind(("0.0.0.0",8000))
tcp_socket.listen()
(comm_socket,client_addr) = tcp_socket.accept()
comm_socket.recv(4096)
```

client

```python
from socket import *
sock_object = socket(AF_INET,SOCK_DGRAM)
sock_object.sendto(b"hello",("127.0.0.1",8000))
```

Resources: 
https://docs.python.org/3/library/socket.html