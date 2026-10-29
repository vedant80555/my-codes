
INF = 999  # Represents infinity (no direct connection)

# Take the total number of routers in the network
n = int(input("Enter number of routers: "))

# Store the direct communication cost between every pair of routers
# Enter INF when there is no direct link between two routers
cost = []
for i in range(n):
    row = input(f"Enter costs for router {i} (use INF for no link): ").split()
    cost.append([INF if x.upper() == "INF" else int(x) for x in row])

# Initially, each router knows only the direct link costs
distance = [row[:] for row in cost]

# Store the next router to visit for reaching each destination
# -1 means that no next hop is known
next_hop = [
    [j if i != j and cost[i][j] != INF else (i if i == j else -1)
     for j in range(n)]
    for i in range(n)
]

# The cost of reaching the same router is always zero
for i in range(n):
    distance[i][i] = 0

# This function prints the routing table of every router
def show_tables(title):
    print("\n" + title)

    for i in range(n):
        print(f"\nRouting Table for Router {i}")
        print("Destination\tCost\tNext Hop")

        for j in range(n):
            # Display INF instead of the internal value 999
            c = "INF" if distance[i][j] == INF else distance[i][j]
            h = "-" if next_hop[i][j] == -1 else next_hop[i][j]
            print(f"{j}\t\t{c}\t{h}")

# Display the original network cost matrix
print("\nInitial Cost Matrix")
for row in cost:
    print(["INF" if x == INF else x for x in row])

# Show routing tables before route updates
show_tables("Initial Routing Tables")

# Keep updating routes while a shorter path is found
updated = True
while updated:
    updated = False

    for i in range(n):
        for j in range(n):
            for k in range(n):

                # Check whether router i can reach k directly
                # and router k can reach destination j
                if cost[i][k] != INF and distance[k][j] != INF:
                    new_cost = cost[i][k] + distance[k][j]

                    # Replace the old route if the new route is cheaper
                    if new_cost < distance[i][j]:
                        distance[i][j] = new_cost
                        next_hop[i][j] = k
                        updated = True

# Display the final routing tables after all updates
show_tables("Final Routing Tables")

# Ask the user to select source and destination routers
src = int(input("\nEnter source router: "))
dest = int(input("Enter destination router: "))

# Ensure the selected routers exist
if not (0 <= src < n and 0 <= dest < n):
    print("Invalid router number")

# Check whether a route exists between the selected routers
elif distance[src][dest] == INF:
    print("No path exists")

else:
    # Begin the path with the source router
    path = [src]
    current = src

    # Follow next-hop entries until the destination is reached
    while current != dest:
        current = next_hop[current][dest]

        # Stop if no valid next hop exists or a loop is found
        if current == -1 or current in path:
            print("Path cannot be determined")
            break

        path.append(current)

    else:
        # Print the minimum cost and the complete route
        print("Minimum Cost:", distance[src][dest])
        print("Shortest Path:", " -> ".join(map(str, path)))

input:
Enter number of routers: 4
Enter costs for router 0 (use INF for no link): 0 2 INF INF
Enter costs for router 1 (use INF for no link): 2 0 3 8
Enter costs for router 2 (use INF for no link): INF 3 0 1
Enter costs for router 3 (use INF for no link): INF 8 1 0


Enter source router: 0
Enter destination router: 3

Minimum Cost: 6
Shortest Path: 0 -> 1 -> 2 -> 3

# ass 2
TCP Socket Programming (Chat Application)


import socket

HOST = "127.0.0.1"  # Local computer IP address
PORT = 5001         # Port used for communication

# Create a TCP socket using IPv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow the port to be reused after the program closes
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Assign the IP address and port to the server
server.bind((HOST, PORT))

# Start listening for a client connection
server.listen(1)
print("TCP Server is waiting for connection...")

# Accept the incoming client connection
# conn is used to communicate; addr stores client address
conn, addr = server.accept()
print("Connected by:", addr)

try:
    while True:
        # Receive a message from the client (maximum 1024 bytes)
        data = conn.recv(1024)

        # Stop if the client disconnects
        if not data:
            break

        # Convert received bytes into a string
        message = data.decode()
        print("Client:", message)

        # Close the conversation when client sends exit
        if message.lower() == "exit":
            conn.sendall("Goodbye!".encode())
            break

        # Ask the server user to type a reply
        reply = input("Server: ")

        # Convert reply into bytes and send it to the client
        conn.sendall(reply.encode())

finally:
    # Close the connected client socket
    conn.close()

    # Close the main server socket
    server.close()
    print("Server closed.")
  
# client

import socket

HOST = "127.0.0.1"  # Address of the server
PORT = 5001         # Must match the server port

# Create a TCP client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Establish a connection with the server
client.connect((HOST, PORT))

try:
    while True:
        # Read a message from the client user
        message = input("You: ")

        # Send the message as bytes to the server
        client.sendall(message.encode())

        # Receive the server's response
        data = client.recv(1024)
        print("Server:", data.decode())

        # Stop after receiving the reply to exit
        if message.lower() == "exit":
            break

finally:
    # Release the client socket
    client.close()
 #inputs:
python server.py
python client.py
You: Hello
Server: Hi
You: How are you?
Server: Fine
You: exit
Server: Goodbye!

TCP Server is waiting for connection...
Connected by: ('127.0.0.1', ...)
Client: Hello
Server: Hi
Client: How are you?
Server: Fine
Client: exit
Server closed.

  # TCP Socket Programming (Mathematical Operations)
  
import socket

HOST = "127.0.0.1"  # Local computer IP
PORT = 5002         # Port for mathematical operations

# Create a TCP server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow the port to be reused after closing
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the server to its IP address and port
server.bind((HOST, PORT))

# Wait for a client to connect
server.listen(1)
print("Math Server is waiting...")

# Accept the client connection
conn, addr = server.accept()
print("Connected to:", addr)

try:
    while True:
        # Receive the calculation from the client
        data = conn.recv(1024)

        # Stop if the client disconnects
        if not data:
            break

        message = data.decode()

        # Exit when the client sends the exit command
        if message.lower() == "exit":
            conn.sendall("Goodbye!".encode())
            break

        try:
            # Split input such as '10 + 5' into three parts
            a, op, b = message.split()

            # Convert both operands into numbers
            a = float(a)
            b = float(b)

            # Perform the operation requested by the client
            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            elif op == "*":
                result = a * b
            elif op == "/":
                # Division by zero is not allowed
                if b == 0:
                    result = "Cannot divide by zero"
                else:
                    result = a / b
            else:
                result = "Invalid operation"

        except ValueError:
            # Handle malformed input, such as 'hello'
            result = "Invalid input. Example: 10 + 5"

        # Convert the result to text and send it back
        conn.sendall(str(result).encode())

finally:
    # Close the client connection and server socket
    conn.close()
    server.close()
    print("Server closed.")


import socket

HOST = "127.0.0.1"  # Server IP address
PORT = 5002         # Must match the server port

# Create a TCP socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the running math server
client.connect((HOST, PORT))

try:
    while True:
        # Ask the user for a calculation or exit
        message = input("Enter calculation (e.g. 10 + 5) or exit: ")

        # Send the calculation to the server
        client.sendall(message.encode())

        # Receive and display the server's answer
        result = client.recv(1024).decode()
        print("Result:", result)

        # End the program after the exit response
        if message.lower() == "exit":
            break

finally:
    # Close the client socket
    client.close()

# inputs 
Enter calculation (e.g. 10 + 5) or exit: 10 + 5
Result: 15.0
Enter calculation (e.g. 10 + 5) or exit: 20 - 8
Result: 12.0
Enter calculation (e.g. 10 + 5) or exit: 6 * 4
Result: 24.0
Enter calculation (e.g. 10 + 5) or exit: 20 / 0
Result: Cannot divide by zero
Enter calculation (e.g. 10 + 5) or exit: exit
Result: Goodbye!

# 3 UDP Socket Programming (Reverse the String)

import socket

HOST = "127.0.0.1"  # Local computer IP address
PORT = 5004         # Port used by this UDP server

# Create a UDP socket using IPv4
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket so the client can send messages to this port
server.bind((HOST, PORT))
print("UDP Server is waiting...")

try:
    while True:
        # Receive message and the client's address
        data, address = server.recvfrom(1024)

        # Convert the received bytes into a string
        message = data.decode()

        # Reply and stop when the client sends exit
        if message.lower() == "exit":
            server.sendto("Goodbye!".encode(), address)
            break

        print("Client:", message)

        # Reverse the order of characters in the string
        result = message[::-1]

        # Send the reversed string back to the client
        server.sendto(result.encode(), address)

finally:
    # Close the UDP socket
    server.close()
    print("Server closed.")


import socket

HOST = "127.0.0.1"  # Address of the server
PORT = 5004         # Must match the server port

# Create a UDP client socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        # Read a string from the user
        message = input("Enter a string (or exit): ")

        # Send the string to the server's IP address and port
        client.sendto(message.encode(), (HOST, PORT))

        # Receive the reply from the server
        data, address = client.recvfrom(1024)
        print("Server reply:", data.decode())

        # Stop after receiving the reply to exit
        if message.lower() == "exit":
            break

finally:
    # Close the client socket
    client.close()

input:
Enter a string (or exit): Hello
Server reply: olleH
Enter a string (or exit): Python
Server reply: nohtyP
Enter a string (or exit): exit
Server reply: Goodbye!

UDP Server is waiting...
Client: Hello
Client: Python
Server closed.

#UDP Socket Programming (Uppercase to Lowercase)

import socket

HOST = "127.0.0.1"  # Local computer IP address
PORT = 5005         # Port for the UDP server

# Create a UDP socket using IPv4
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the selected IP address and port
server.bind((HOST, PORT))
print("UDP Server is waiting...")

try:
    while True:
        # Receive the client's message and address
        data, address = server.recvfrom(1024)

        # Decode bytes into a readable string
        message = data.decode()

        # Stop when the client requests exit
        if message.lower() == "exit":
            server.sendto("Goodbye!".encode(), address)
            break

        print("Client:", message)

        # Convert uppercase letters to lowercase
        result = message.lower()

        # Send the converted string back to the client
        server.sendto(result.encode(), address)

finally:
    # Release the server socket
    server.close()
    print("Server closed.")


import socket

HOST = "127.0.0.1"  # Address of the UDP server
PORT = 5005         # Must match the server port

# Create a UDP client socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        # Input a string from the user
        message = input("Enter a string (or exit): ")

        # Send the string to the server
        client.sendto(message.encode(), (HOST, PORT))

        # Receive the converted string
        data, address = client.recvfrom(1024)
        print("Server reply:", data.decode())

        # Exit after receiving the server's reply
        if message.lower() == "exit":
            break

finally:
    # Close the client socket
    client.close()
#
python server.py
python client.py
Enter a string (or exit): HELLO WORLD
Server reply: hello world
Enter a string (or exit): PYTHON PROGRAMMING
Server reply: python programming
Enter a string (or exit): exit
Server reply: Goodbye!

#Hamming Code (Error Detection and Correction)


# Hamming Code: Error Detection and Correction

# Take original binary data from the user
data = input("Enter data bits (e.g. 1011): ")

# Check that input contains only 0 and 1
if not data or any(bit not in "01" for bit in data):
    print("Enter only 0 and 1.")
    raise SystemExit

m = len(data)  # Number of original data bits
r = 0           # Number of parity bits required

# Calculate parity bits using 2^r >= m + r + 1
while 2 ** r < m + r + 1:
    r += 1

n = m + r  # Total bits in the Hamming codeword

# Use positions starting from 1 for easier parity calculation
code = [0] * (n + 1)

# Place data bits in positions that are not powers of 2
# Positions 1, 2, 4, 8, ... are reserved for parity bits
j = 0
for i in range(1, n + 1):
    if i & (i - 1):  # True for non-parity positions
        code[i] = int(data[j])
        j += 1

# Calculate even parity bits at positions 1, 2, 4, 8, ...
for p in range(r):
    pos = 2 ** p
    parity = 0

    # Check every bit position covered by this parity bit
    for i in range(1, n + 1):
        if i & pos:
            parity ^= code[i]  # XOR calculates even parity

    # Store the calculated parity bit
    code[pos] = parity

# Display the transmitted codeword from left to right
word = "".join(str(code[i]) for i in range(n, 0, -1))
print("Transmitted codeword:", word)

# Enter received codeword, or press Enter to simulate no error
received = input("Enter received codeword (Enter for no error): ")

if received == "":
    received = word

# Check that the received codeword has the correct format
if len(received) != n or any(bit not in "01" for bit in received):
    print("Invalid received codeword!")
    raise SystemExit

# Store received bits in their numbered positions
# The rightmost bit is position 1
for i in range(1, n + 1):
    code[i] = int(received[n - i])

# Check parity again to calculate the error syndrome
error_pos = 0
for p in range(r):
    pos = 2 ** p
    parity = 0

    # Recalculate parity using the received bits
    for i in range(1, n + 1):
        if i & pos:
            parity ^= code[i]

    # A failed parity check contributes to the error position
    if parity:
        error_pos += pos

# Correct the bit if a single-bit error is detected
if error_pos == 0:
    print("No error detected.")
else:
    print("Error detected at position:", error_pos)

    # Flip the incorrect bit: 0 becomes 1 or 1 becomes 0
    code[error_pos] ^= 1

    # Display the corrected codeword
    print("Corrected codeword:",
          "".join(str(code[i]) for i in range(n, 0, -1)))

# Extract data bits by skipping parity positions
decoded = ""
for i in range(1, n + 1):
    if i & (i - 1):
        decoded += str(code[i])

# Display the recovered original data
print("Received data:", decoded)

input:
python hamming.py
Enter data bits (e.g. 1011): 1011

Transmitted codeword: 1100110
Enter received codeword (Enter for no error):

Case 2 — Data received correctly
    No error detected.
Received data: 1011

Single-bit error at position 1
  Enter data bits (e.g. 1011): 1011
Transmitted codeword: 1100110
Enter received codeword (Enter for no error): 1100111
Error detected at position: 1
Corrected codeword: 1100110
Received data: 1011

Case 4 — Single-bit error at position 3
Run it again and enter 1100010.

Enter data bits (e.g. 1011): 1011
Transmitted codeword: 1100110
Enter received codeword (Enter for no error): 1100010
Error detected at position: 3
Corrected codeword: 1100110
Received data: 1011





