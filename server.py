import threading
import socket

host = "127.0.0.1" # change this to server ip upon implementation
port = 55555

# Create the server socket for TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket
server.bind((host, port))
# Server now listening for connections.
server.listen()

# Lists to store clients and their associated aliases.
clients = []
aliases = []

def broadcast(message):
    """
    Parameters: Message to send to all clients.

    Function: This function will broadcast a message to all the clients
    who are connected.
    """
    # For each client in the clients list, send the message to them.
    for client in clients:
        client.send(message)

def private_message(message, alias):
    """
    Parameters: Message to send to the designated client. Alias, which 
    indicates which client you'd like to message.

    Function: This function will broadcast a message to all the clients
    who are connected.
    """
    # Find the index of the client through the aliases list.
    index = aliases.index(alias)
    # Find the designated client using the found index.
    client = clients[index]
    # Send the message to the designated client.
    client.send(message)

def handle(client):
    # While the application is running, do this.
    while True:
        # Try and receive messages from the client.
        try:
            # Receive the message from the client. Standard 1024 Bytes.
            message = client.recv(1024)
            # Broadcast the message to the other clients. No need to encode since we didn't decode.
            broadcast(message)
        except:
            # Grab the index of the client from the list
            index = clients.index(client)
            # Remove the client from the client list
            clients.remove(client)
            # Close the client connection
            client.close()
            # Retrieve the alias of the client using the index we retrieved.
            alias = aliases[index]
            # Broadcast that the client has disconnected. Need to encode the message before sending.
            broadcast(f"{alias} has left the chat.".encode('utf-8'))
            # Remove the alias from the aliases list.
            aliases.remove(alias)
            # Break out of the loop
            break

def receive():
    """
    This function will allow for the server to receive messages
    from the clients and distribute the messages through the handle function.
    """
    # While the application is running, do this.
    while True:
        # Accept the client port and address.
        client, address = server.accept()
        # Print to the console that a client has connected.
        print(f"Connected with {str(address)}")

        # Prompt the client who joined to enter their alias.
        client.send("Enter your alias: ".encode('utf-8'))
        # Store the client alias in a variable.
        alias = client.recv(1024).decode('utf-8')
        # Append the chosen alias to the alias list.
        aliases.append(alias)
        # Append the client socket to the clients list.
        clients.append(client)

        # Print the chosen alias to the console.
        print(f"Alias of the client is: {alias}!")\
        # Broadcast to all clients that a new user with the chosen alias has connected.
        broadcast(f"{alias} has connected to the server!".encode("utf-8"))

        # Notify the client that they have successfully connected to the server.
        client.send("You have successfully connected to the server!".encode('utf-8'))

        # Create a thread to handle the communication for this client.
        thread = threading.Thread(target = handle, args = (client,))
        # Start the thread.
        thread.start()

# Print to the console that the server is running.
print("Server is live. Listening for Clients...")
# Call the receive function to start the services.
receive()