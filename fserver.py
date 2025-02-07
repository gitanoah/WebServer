#first server using python
#Noah Angus// From Youtube Rivaan Ranawat
import socket
import time

#incase port changes bc of restraints or something to prevent hassle I split socket bind into S_H & S_P
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 7777

#socket allow transfer of data from different inputs
#ipv4 address

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_HOST, SERVER_PORT))

#listen for requests
server_socket.listen(5)

print(f'Listening on port {SERVER_PORT}...')

#or SOCK_DGRAM - udp
#SOCK_STREAM - tcp socket(connection)

#CLIENTE INTERACTION AND QUE (send and recieve data)

#loop listens for multiple connection rather than 1
#get data or http request from client to give appr response using .RECV()
while True:  
    client_socket, client_address = server_socket.accept()
    req = client_socket.recv(1500).decode()
    print(req)

    #got python to return data related to client

    
##print(client_socket)
##print(client_address)

#print(slient)
