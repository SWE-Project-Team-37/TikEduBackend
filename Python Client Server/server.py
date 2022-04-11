import socket as sock
import gzip
from _thread import *

# Function to define the behavior of each thread/client
def fileTransferThread(connection):
    while True:
        # Obtain request details from client side and call proper sections
        #messageFromClient = connection.recv(1024).decode()
        messageFromClient = connection.recv(1024)
        messageFromClient = gzip.decompress(messageFromClient).decode('utf-8')
        #messageFromClient = str(connection.recv(1024))

        print("messageFromClient: " + messageFromClient)
        if messageFromClient == "exit":
            print("Client has disconnected.\n")
            break

        try:
            myCommand = messageFromClient.split()[0]
            fileName = messageFromClient.split()[1]
        except: 
            print("Message from client222: ", messageFromClient)
            return 

        if myCommand == "get":

            # Print message on server side terminal
            print("File to be downloaded =", fileName)

            # Open the file to download
            myFile = open(fileName, "rb")

            # Read from file and send data to the client until no data is left
            while True:
                dataToSend = myFile.read(1024)
                if not dataToSend:
                    break
                connection.send(dataToSend)
                if len(dataToSend) < 1024:
                    break

            # Close the file
            myFile.close()

            # Print message on server side terminal to indicate file transfer complete
            print("File has been downloaded successfully. \nPlease return to the client or connect a new client to this server. \n")

        elif myCommand == "upload":

             # Print message on server side terminal
            print("File to be uploaded =", fileName)

            # Open a file to write to with proper name
            newFilename = "new" + fileName
            myFile = open(newFilename, "wb")

            # Receive data from the client and write to file until no more data is received
            while True:
                receivedData = connection.recv(1024)
                if not receivedData:
                    break
                myFile.write(receivedData)
                if len(receivedData) < 1024:
                    break

            # Once file has been downloaded completely, close file
            myFile.close()

            # Print message on server side terminal to indicate file transfer complete
            print("File has been uploaded successfully. \nPlease return to the client or connect a new client to this server. \n")

    
            
# Driver code for server

# Variables
#HOST, PORT = "153.33.76.164", 8080
#HOST, PORT = "0.0.0.0", 8080
HOST, PORT = "192.168.1.9", 8080
print("\nWelcome to the TikEdu server!\n")

# Create socket and accept connections
mySocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
mySocket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, 1)
mySocket.bind((HOST, PORT))
mySocket.listen(3) # Specify number of permitted unaccepted connection requests
#mySocket.connect((HOST, PORT))
numAttemptedClients = 0

while True:
    try:
        connection, address = mySocket.accept()
        numAttemptedClients += 1 # Increment number of clients
        print("------------Client " + str(numAttemptedClients) + " connected------------")
        print("Connection from client: " + str(address))
        start_new_thread(fileTransferThread, (connection,))
        
        #req = connection.recv(1024).decode()
        #print("\nreq = ", req)
    except: 
        # FIXME numClients is not decremented when client disconnects
        "In try block with exception #" + str(numAttemptedClients)

