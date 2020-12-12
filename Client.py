import socket
import sys
import os
import pathlib
clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect(("localhost",5500))
argv=sys.argv
path=pathlib.Path(argv[1])
filename=path.name
print("Filename : ",filename)
print()
clientSocket.sendall(bytes(str(len(filename)).ljust(100),"utf-8"))
responseDataBytes=b''
toRecv=100
while len(responseDataBytes)<toRecv:
    by=clientSocket.recv(toRecv-len(responseDataBytes))
    responseDataBytes+=by
response=responseDataBytes.decode("utf-8").strip()
print(response)
print()
print("Sending filename to server...")
print()
clientSocket.sendall(bytes(filename,"utf-8"))
responseDataBytes=b''
toRecv=100
while len(responseDataBytes)<toRecv:
    by=clientSocket.recv(toRecv-len(responseDataBytes))
    responseDataBytes+=by
response=responseDataBytes.decode("utf-8").strip()
print(response)
print()
file=open(path,"rb")
dataBytes=file.read()
file.close()
print("Length of data in file : ",len(dataBytes))
print()
clientSocket.sendall(bytes(str(len(dataBytes)).ljust(100),"utf-8"))
responseDataBytes=b''
toRecv=100
while len(responseDataBytes)<toRecv:
    by=clientSocket.recv(toRecv-len(responseDataBytes))
    responseDataBytes+=by
response=responseDataBytes.decode("utf-8").strip()
print(response)
print()
print("Sending file to server...")
print()
chunkSize=4086
toSend=len(dataBytes)
dataSend=0
while dataSend<toSend:
    if toSend-dataSend<chunkSize: chunkSize=toSend-dataSend
    print(f"sending chunk size to server : {chunkSize}")
    clientSocket.sendall(bytes(str(chunkSize).ljust(100),"utf-8"))
    responseDataBytes=b''
    toRecv=100
    while len(responseDataBytes)<toRecv:
        by=clientSocket.recv(toRecv-len(responseDataBytes))
        responseDataBytes+=by
    response=responseDataBytes.decode("utf-8").strip()
    print(response) 
    print()
    data=dataBytes[dataSend:dataSend+chunkSize]
    dataSend+=chunkSize
    clientSocket.sendall(data)
    responseDataBytes=b''
    toRecv=100
    while len(responseDataBytes)<toRecv:
        by=clientSocket.recv(toRecv-len(responseDataBytes))
        responseDataBytes+=by
    response=responseDataBytes.decode("utf-8").strip()
    print(response) 
    print()
print("Data send from client side,Waiting for the final response of server...")
responseDataBytes=b''
toRecv=100
while len(responseDataBytes)<toRecv:
    by=clientSocket.recv(toRecv-len(responseDataBytes))
    responseDataBytes+=by
response=responseDataBytes.decode("utf-8").strip()
print(response)
print()
print("Response received from the server and file transferd complitly")
clientSocket.close()
