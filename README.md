Pink Floyd - Client-Server Project
Project Overview
  This project implements a client-server model that allows clients to request information about Pink Floyd songs stored in a data file. 
  The communication between the client and server is handled using Python's sockets library.

Features
  1. Server: Hosts a database (data file) of Pink Floyd songs and responds to client requests with information.
  2. Client: Connects to the server and sends queries to retrieve song details.
  3. Data File: Contains structured information about various Pink Floyd songs, such as title, album, release date, and song length.
     
Technology Stack
  1. Python: The project is written entirely in Python.
  2. Sockets Library: Used to manage client-server communication.
  3. File I/O: The server reads song data from a file.
     
Project Structure
  1. server.py: Handles client connections, reads the data file, and responds to client requests.
  2. client.py: Connects to the server, sends song queries, and displays the results.
  3. data.txt: Contains information about Pink Floyd songs in a structured format.
     
How It Works
  1. The server reads the song information from the data.txt file and listens for incoming client connections.
  2. The client connects to the server using sockets and sends queries (e.g., song title).
  3. The server processes the query, retrieves the matching song details, and sends the information back to the client.
  4. The client displays the retrieved song information.
