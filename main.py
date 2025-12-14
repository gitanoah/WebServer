## Guided by Build Your Own Web Server from Scratch using Python! - Rivaam Ranawat
import socket
import time

SERVER_HOST = "0.0.0.0" 
SERVER_PORT = 8000

#Step 1

# AF_INET specifies IP version for addresses, IPv4 is first stable version and most used
# SOCK_STREAM means it is a TCP socket, establishes connection between sender and reciever and verifies data
# SOCK_DGRAM is for UDP, sends data grams without verifiying if recipient is ready or not

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#server_socket.setblocking(False) - from step 3

#Step 2

server_socket.bind((SERVER_HOST, SERVER_PORT))

#so only 5 connections can be queued
server_socket.listen(5)

print(f"Listening on port {SERVER_PORT}...")

#Step 3
while True:
    client_socket, client_address = server_socket.accept()
    request = client_socket.recv(1500).decode()
    print(request)

    #since http version 1.1 all requests have same structure, we can extract info from headers w/ list

    headers = request.split('\n')
    first_headers_component = headers[0].split()

    http_method = first_headers_component[0]
    path = first_headers_component[1]

    if http_method == "GET":
        if path == '/':
            fin = open("index.html")

            #Status line
            #Headers
            #Message-Body
        

        #more of these would be like a full fledge web server
        elif path == '/book':
            fin = open("book.json")
        else:
            fin = open("404.html")
        content = fin.read()
        fin.close()
        response = 'HTTP/1.1 200 OK\n\n' + content
    
    else:
        response = 'HTTP/1.1 405 Method Not Allowed\n\nAllow: GET'    
    
    client_socket.sendall(response.encode())
    client_socket.close()
