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
		- If a client intentionally delays or doesn't complete the TCP handshake process, the connection slots in the queue will remain filled preventing actual clients from connecting or starting the handshake process.
	
	- 3. **Application of Security Category** (Confidentiality, Integrity, or Availability)
		- **Availability**
	
	- 4. **Test Goal**
		- Determine if a single user can occupy connection slots in a way that interferes with new clients connections.
	
	- 5. **Reflection**
		- **Expected Observations**:
			**If Correct Hypothesis**
			- New clients will experience delayed connections or connection refusals.
			- They will experience a blank buffering and no HTTP response at all, it won't even reach the 404 error screen (since to HTTP response is able to be returned it is still waiting on `recv()` from the first connection).
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
	
