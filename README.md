# WebServer
Making a web server in python
Then performing a security analysis on it
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
		- CORS - mechanism allowing restricted resources on a webpage to be requested from another domain outside the domain from which the first resource was
		- making sure you can only request data from that website, not from another site directly, protecting visitors from malicious scripts or data thefts
	- **Sec-Fetch-Dest: document** - type of content client expects to receive from request
##  HTTP Response
- responses also have a structure
- First - STATUS LINE: w/ Http Version, Status code (e.g. '200' means everything went well), and Optional Text Message
- Second - Has some headers passed to it, similar to request headers
- Third - Message body (optional)

#Evaluating Web Server
  **Pre-Notes: **
- **Steps**
	1. Observation
	2. Assumptions
	3. Hypothesis
	4. Security Category
	5. Test Goal
	6. Reflection
- **(*OWASP*) Application of Security Categories - CIA Triad** 
	- 1 **C**onfidentiality - protection of data
	- 2 **I**ntegrity - protection against unauthorized modification
	- 3 **A**vailability - insurance of presence of information or resources


## Initial Observations 
### Connection Queue Limit (*Making Socket Listen*)
- The server can set a max number of connections when `.listen()` is called
- TCP connection attempts beyond the set limit are either temporarily ignored or refused

	- 1. **Assumptions:**
		- Clients will separately complete the TCP connection handshake. 
		- Connection spots in the listen queue will be free.
	
	- 2. **Hypothesis:**
		- If a client intentionally completes the TCP handshake but doesn't send application-layer data, the connection slots in the queue will remain filled (server will block off `recv()`) preventing actual clients from connecting or starting the handshake process.
	
	- 3. **Application of Security Category** (Confidentiality, Integrity, or Availability)
		- **Availability**
	
	- 4. **Test Goal**
		- Determine if a single user can occupy connection slots in a way that interferes with new clients connections.
	
	- 5. **Reflection**
		- **Expected Observations**:
			**If Correct Hypothesis**
			- New clients will experience delayed connections or connection refusals.
			- They will experience a blank buffering and no HTTP response at all, it won't even reach the 404 error screen (since no HTTP response is able to be returned it is still waiting on `recv()` from the first connection).
		    **If Incorrect Hypothesis**
		    - New clients will connect to the server and access HTTP responses.
		    - Minimal delay and no connection refusals.
		- **Test Design:**
			- I first established a normal connection to the web server by accessing it through a browser after running it from VS Code
			- To target connection handling at TCP layer (before accessing HTTP responses) I connected using ***Netcat*** from a Kali Linux Virtual Machine: `nc <server-ip> 8000` 
				- This was in order to open a TCP connection, and after the handshake process not sending HTTP data to the server (OWASP Testing Guide v2)
			- I then tried to connect to the server on my laptop from a google chrome browser using `localhost:8000`
		- **Results:**
			- **Browser Alone:** When I connected as a client from the browser I successfully connected to the server, sent a HTTP request, and received a response which was the home screen saying it was `Noah's Own Web Server`

			- **NetCat with Browser:** When I connected initially through NetCat and then attempted to connect as a client from my browser using "localhost:8000" the server buffered and did not allow the client to complete their connection.
				- However whenever I sent a HTTP request from NetCat `GET / HTTP/1.1` the server responded with `HTTP/1.1 200 OK` and the client's connection was completed shortly after.
		- **Conclusion & Lessons Learned:**
			- Weakness
				- The server handles connections one by one and blocks indefinitely on `recv()`, which allows a single client to impact availability.
			- Potential Improvements
				- Add a socket timeout to limit how long the server waits on a clients data.
				- Handle each client connection in a separate process.
				- Limit how long a connection may remain idle.
			- Key Takeaways
				- Availability vulnerabilities can exist even in simple systems.
				- Network layer behavior can prevent the execution of application layer logic.
	
