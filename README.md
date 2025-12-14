# WebServer
Me trying to make a web server in python (so I don't forget the language)
Then penetrating the server using a VM (Kali Linux)
*These are my attached notes for both parts, code is attached from VS Code File*

**Web Server** - system that stores processes and delivers web pages to users, done usually using http (hyper text transfer protocol)
## Step 1: Create and Initialize Socket

- Socket is an endpoint in a network communication system
- Allow data to be sent and received over network
- Facilitate connection between multiple clients and server
- *http* - protocol used when data is sent or received in between sockets

### socket()
- **family** - accepts type of address family, in this case an IP
	- IP (Internet Protocol) - rules for routing or sending packets of data across networks between devices, make sure data packets are routed to correct place
- **type** - accepts type of socket
	- **TCP** - Transmission control protocol
	- 3 step process, SYN (request by sending SYN packet set to server), SYN-ACK (server responds with this packet, acknowledging the SYN packet), ACK (client receives servers SYN-ACK packet and responds with ACK packet) and can now start exchanging data.
	- **UDP** - user datagram protocol, datagrams are sent without the handshake process, so its faster but no guarantee if or how packets will arrive
	- Generally used in live video, audio, or online games
### Socket Options
- level - protocol level for which configuration happens
- option name - feature to enable by value (ex: SO_REUSEADDR)
	- allows endpoint to be reused immediately after socket is closed (normally a delay before endpoint can be reused to make sure delayed packets are mistakenly delivered to wrong application)

## Step 2: Bind Socket to Our Computer
### Binding
- With IP address and Port
- **IP Address** - unique numbers and letters that locate a device on a network
	- DNS - domain name system, maps string to IP address of website (like google.com -> numbers (142.250......) )
- **Port** - helps differentiate between multiple services on same computer, routing to correct application, ports 0 - 1023 are reserved for operating systems used
### Making Socket Listen
- Creates a queue for connections handling the 3 step handshake
- can also specify size of queue, if full client will have to try later because request is either ignored or refused

## Step 3: Accepting Connections
- connections are in a queue, so .accept() to get first element of queue
- code is blocked until it reaches a request unless you set the blocking to false (port.setblocking(False))
	- however, unless you catch the exception you will get an error because head of queue is null
## Get HTTP Request from Client
- HTTP Request Structure
	- first line is request line, including  1. http method (in my case 'GET') 2. is path (route in site where you are trying to go, in this case '/') 3. last is HTTP version used to send request (***version determines structure of rest of request***)
	- We get http 1.1 requests (and not http 2 or http 3) because we created a basic server relying on tcp because http 3 isn't used
		- for http 3 we would need to depend on QUIC
		- for http 2 we would need other protocols that would be able to accept multiple requests at once (multiplexing)
	- **Set-Fetch-Mode: Navigate** - specifies mode for how request should be made regarding CORS (cross origin resource sharing) protocol, security mechanism by web browsers protecting users from certain types of cyber attacks


