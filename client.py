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
        
def dehash(alias, message):
    """
    This function will dehash the message received from other clients.
    """
    # Hash method is replacing vowels with consonants.
    vowels = 'aeiou'
    # Consonants to replace vowels with
    replace = '@#$%^'
    # Go through each letter in the message
    for letter in message:
        # Go through the list of vowels and compare them to the letter from message.
        for vowel in vowels:
            if letter == vowel:
                index = vowels.index(vowel)
                # Replace vowel with consonant
                message = message.replace(letter, replace[index])
    newMessage = f"{alias}: {message}"  
    return newMessage

def write():
    """
    This function is how the client will create their message and send it
    to the server to be passed on to the client or clients identified.
    """
    # Do this while the application is running
    while True:
        # Prompt the user for the message.
        message = f"{input('')}"
        # Send the message and encode it.
        hashedMessage = hash(alias, message)
        client.send(hashedMessage.encode('utf-8'))

def hash(alias, message):
    """
    This function will do a simple mock hack on the messages
    sent from one client to the others. This "hashing" is strictly used
    for wireshark debugging.
    """
    # Hash method is replacing vowels with symbols.
    vowels = 'aeiou'
    # Symbols to replace vowels with
    replace = '@#$%^'
    # Go through each letter in the message
    for letter in message:
        # Go through the list of vowels and compare them to the letter from message.
        for vowel in vowels:
            if letter == vowel:
                index = vowels.index(vowel)
                # Replace vowel with symbol
                message = message.replace(letter, replace[index])
    newMessage = f"{alias}: {message}"  
    return newMessage

# Create a thread for receiving messages and start it.
receive_thread = threading.Thread(target = receive)
receive_thread.start()

# Create a thread for writing/sending messages and start it.
write_thread = threading.Thread(target = write)
write_thread.start()