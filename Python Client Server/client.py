import socket as sock
import os.path


# --------Function to print the format of the input required from use--------
def printInstructions():
    print("\n")
    print("-------------------File Transfer Commands-------------------")
    print("To upload a file to the server, type: 'upload <fileName>'")
    print("To download a file from the server, type: 'get <fileName>'")
    print("To exit the file transfer service, type: 'exit'")
    print("\n")


# -----------------Function to get/download file from server-----------------
def downloadFileFromServer(filename, mySocket):
    messageToServer = "get " + filename
    mySocket.send(bytes(messageToServer, "utf-8"))

    # Open a file to write to with proper name
    newFilename = "new" + filename
    myFile = open(newFilename, "wb")

    # Receive data from the server and write to file until no more data is received
    while True:
        receivedData = mySocket.recv(1024)
        if not receivedData:
            break
        myFile.write(receivedData)
        if len(receivedData) < 1024:
            break

    # Once file has been downloaded completely, close file
    myFile.close()


# -------------------Function to upload file from server---------------------
def uploadFileToServer(fileName, mySocket):
    messageToServer = "upload " + fileName
    mySocket.send(bytes(messageToServer, "utf-8"))

    # Open the file to read from
    myFile = open(fileName, "rb")

    # Receive data from the server and write to file until no more data is received
    while True:
        dataToSend = myFile.read(1024)
        if not dataToSend:
            break
        mySocket.send(dataToSend)
        if len(dataToSend) < 1024:
            break

    # Once file has been downloaded completely, close file
    myFile.close()


# --------------------------Start of program--------------------------

# Connect to the server
mySocket = sock.socket()
mySocket.connect(("153.33.76.164", 8080))

print("\nWelcome to the multithreaded file transfer service! You are one (of many possible) client(s).")
printInstructions()
programActive = 1

while programActive == 1:
    myRequest = input()

    if myRequest == "exit":
        # close socket
        programActive = 0
        print("Thank you for using the multithreaded file transfer service. Goodbye.")
        mySocket.send(bytes(myRequest, "utf-8"))
        break
    else:
        myCommand = myRequest.split()[0]
        fileName = myRequest.split()[1]

        if myCommand == "get":
            downloadFileFromServer(fileName, mySocket)
        elif myCommand == "upload":
            uploadFileToServer(fileName, mySocket)

    print("File Transfer Request Completed. ")
    printInstructions()










