# import socket module
from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
# Fill in start
serverPort = 12000
serverSocket.bind(('192.168.1.2', serverPort))
serverSocket.listen(1)
# Fill in end

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()  # Fill in start #Fill in end
    try:
        message = connectionSocket.recv(1024).decode()  # Fill in start #Fill in end
        print(message)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.readlines()  # Fill in start #Fill in end
        # Send one HTTP header line into socket
        # Fill in start
        connectionSocket.send('HTTP/1.0 200 OK\n'.encode())
        # Fill in end
        # Send the content of the requested file to the client
        connectionSocket.send("\n".encode())
        for i in range(0, len(outputdata)):
            # connectionSocket.send("\n".encode())
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        # Fill in start
        # connectionSocket.send("\n".encode())
        connectionSocket.send('HTTP/1.0 404 Not Found\n'.encode())
        # Fill in end
