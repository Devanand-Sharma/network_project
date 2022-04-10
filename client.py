import socket
import threading

# Prompt the user upon launch for their alias.
alias = input("Enter your alias: ")

# Create the client socket.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect client to the server
client.connect(('127.0.0.1', 55555))

def receive():
    """
    This function will allow the client to receive messages from
    the server which other clients are trying to send them.
    """

    # While the application is running do this.
    while True:
        # Try and receive messages from the server
        try:
            # Receive the message and decode it.
            message = client.recv(1024).decode('utf-8')
            # If the message is the alias prompt from the server, then pass the alias.
            if message == "Enter your alias: ":
                # Send the alias to the server
                client.send(alias.encode('utf-8'))
            # Else we are just printing what the server send us as it's a regular message.
            else:
                print(message)
        # If the receiving message doesn't work, do this.
        except:
            # Notify the client that the connection is going to be closed.
            print("Something went wrong. Closing the connection...")
            # Close the connection.
            client.close()
            # Break out of the loop.
            break

def write():
    """
    This function is how the client will create their message and send it
    to the server to be passed on to the client or clients identified.
    """
    # Do this while the application is running
    while True:
        # Prompt the user for the message.
        message = f"{alias}: {input('')}"
        # Send the message and encode it.
        client.send(message.encode('utf-8'))

# Create a thread for receiving messages and start it.
receive_thread = threading.Thread(target = receive)
receive_thread.start()

# Create a thread for writing/sending messages and start it.
write_thread = threading.Thread(target = write)
write_thread.start()