import socket
import threading

# Define constants for the server
HOST = 'localhost'
PORT = 8000
MAX_CLIENTS = 5

# Create a dictionary to hold all connected clients and their usernames
connected_clients = {}
username_to_socket = {}
usernames_set = set()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#IPv4 addresses,TCP protocol

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()


# Function to handle incoming client connections
def handle_client(client_socket, client_address):
      
    # Prompt the client for their username
    client_socket.send("zPlease enter your username: ".encode())
    username = client_socket.recv(1024).decode()
    while username in usernames_set:
        client_socket.send(
            "zThis username is already taken, please choose another one: ".encode())
        username = client_socket.recv(1024).decode()
        
    if len(connected_clients) < MAX_CLIENTS:
            # Add the client to the dictionary of connected clients
            connected_clients[client_socket] = username
            username_to_socket[username] = client_socket
            usernames_set.add(username)
    else:
            client_socket.send(
            "zThe server is currently busy. Please try again later. ".encode())
            client_socket.close()
    



    # Send a welcome message to the client
    client_socket.send(f"wWelcome to the chat room, {username}!\n".encode())
    client_socket.send(f"O{','.join(usernames_set)}".encode())
    # This allows all other connected clients to be notified about the new client joining the chat.
    for c in connected_clients.keys():
        if c != client_socket:
            c.send(f"o{username}".encode())

    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode()

            if not data:
                break

            # Broadcast the message to all connected clients
            for c in connected_clients.keys():
                if c != client_socket:
                    c.send(
                        f"n{connected_clients[client_socket]}: {data}".encode())
        except Exception as e:
            print(e)
            # Remove the client from the dictionary of connected clients
            del connected_clients[client_socket]
            del username_to_socket[username]
            usernames_set.remove(username)
            client_socket.close()
            for c in connected_clients.keys():
                c.send(
                    f"o{username}".encode())
            break


# Main loop to handle incoming connections
while True:
    
    # Accept incoming connections
    client_socket, client_address = server_socket.accept()

    # Create a new thread to handle the client connection
    client_thread = threading.Thread(
        target=handle_client, args=(client_socket, client_address))
    client_thread.start()