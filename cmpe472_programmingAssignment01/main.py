from socket import *
import ssl
import base64

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"
# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = 'smtp.gmail.com'  # Fill in start #Fill in end
mailPort = 465
# Create socket called clientSocket and establish a TCP connection with mailserver
# Fill in start
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)
clientSocket.connect((mailserver, mailPort))
# Fill in end

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')
# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
# Fill in start

Username = input("Username: ")
Password = input("Password: ")

authMesg = 'AUTH LOGIN\r\n'
crlfMesg = '\r\n'
clientSocket.send(authMesg.encode('utf-8'))

email = base64.b64encode(Username.encode('utf-8'))
password = base64.b64encode(Password.encode('utf-8'))

clientSocket.send(email)
clientSocket.send(crlfMesg.encode('utf-8'))

clientSocket.send(password)
clientSocket.send(crlfMesg.encode('utf-8'))

fromCmd = 'MAIL FROM: <' + Username + '>\r\n'
clientSocket.send(fromCmd.encode())
recv2 = clientSocket.recv(1024)
if recv2[:3] != '250':
    print('250 reply not received from server.')
else:
    print(recv2)
# Fill in end

# Send RCPT TO command and print server response.
# Fill in start

receiver = Username
# Fill in start
toCmd = 'RCPT TO: <' + receiver + '>\r\n'
clientSocket.send(toCmd.encode())
recv3 = clientSocket.recv(1024)
if recv3[:3] != '250':
    print('250 reply not received from server.')
else:
    print(recv3)

# Fill in end

# Send DATA command and print server response.
# Fill in start

dataCmd = 'DATA\r\n'
clientSocket.send(dataCmd.encode())
recv4 = clientSocket.recv(1024)
print(recv4)

# Fill in end
# Send message data.
# Fill in start

Subject = "CMPE472- Programming Assignment 01- SMTP- Message"
stri = "Subject: " + Subject + "\r\n\r\n" + msg
clientSocket.send(stri.encode())

# Fill in end
# Message ends with a single period.
# Fill in start
clientSocket.send(endmsg.encode())
recv5 = clientSocket.recv(1024)
print(recv5)
# Fill in end
# Send QUIT command and get server response.
# Fill in start
clientSocket.send("QUIT\r\n".encode())
recv6 = clientSocket.recv(1024)
print(recv6)
clientSocket.close()
# Fill in end
