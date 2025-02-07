#first server using python
#Noah Angus// From Youtube Rivaan Ranawat
import socket


#incase port changes bc of restraints or something to prevent hassle I split socket bind into S_H & S_P
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 7777

#socket allow transfer of data from different inputs
#ipv4 address

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_HOST, SERVER_PORT))

#listen for requests
server_socket.listen(5)

print(f'Listening on port {SERVER_PORT}...')

#or SOCK_DGRAM - udp
#SOCK_STREAM - tcp socket(connection)

#CLIENTE INTERACTION AND QUE (send and recieve data)

client_socket, client_address = server_socket.accept()
print(slient)
