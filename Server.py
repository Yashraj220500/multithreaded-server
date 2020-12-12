import socket
import os 
import threading
class MyThread(threading.Thread):
    def __init__(self,serverSocket,clientSocket):
        threading.Thread.__init__(self)
        self.serverSocket=serverSocket
        self.clientSocket=clientSocket
    def run(self):
        requestDataBytes=b''
        toRecv=100
        while len(requestDataBytes)<toRecv:
            by=clientSocket.recv(toRecv-len(requestDataBytes))
            requestDataBytes+=by
        request=requestDataBytes.decode("utf-8").strip()
        filenameLength=int(request)
        print("Length of file : ",filenameLength)
        clientSocket.sendall(bytes("Length of filename received ".ljust(100),"utf-8"))
        requestDataBytes=b''
        toRecv=filenameLength
        while len(requestDataBytes)<toRecv:
            by=clientSocket.recv(toRecv-len(requestDataBytes))
            requestDataBytes+=by
        filename=requestDataBytes.decode("utf-8").strip()
        print("Filename : ",filename)
        clientSocket.sendall(bytes("Name of file received ".ljust(100),"utf-8"))
        requestDataBytes=b''
        toRecv=100
        while len(requestDataBytes)<toRecv:
            by=clientSocket.recv(toRecv-len(requestDataBytes))
            requestDataBytes+=by
        fileDataLength=int(requestDataBytes.decode("utf-8").strip())
        print("File length : ",fileDataLength)
        clientSocket.sendall(bytes("Length of file data received...".ljust(100),"utf-8"))
        requestDataBytes=b''
        toRecv=fileDataLength
        while len(requestDataBytes)<toRecv:
            requestData=b''
            toReceive=100
            while len(requestData)<toReceive:
                b=clientSocket.recv(toReceive-len(requestData))
                requestData+=b
            chunkSize=int(requestData.decode("utf-8"))
            clientSocket.sendall(bytes(f"chunkSize received : {chunkSize}".ljust(100),"utf-8"))
            print("Incoming : ",chunkSize)
            print()
            toReceive=chunkSize
            requestData=b''
            while len(requestData)<toReceive:
                b=clientSocket.recv(toReceive-len(requestData))
                requestData+=b
            clientSocket.sendall(bytes(f"Data of size {chunkSize} received".ljust(100),"utf-8")) 
            requestDataBytes+=requestData
        file=open("c:\\pyeg\\Network\\assignment\\uploads\\"+filename,"wb")
        file.write(requestDataBytes)
        file.close()
        clientSocket.sendall(bytes("File received at server side...".ljust(100),"utf-8"))
        clientSocket.close()
        
serverSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind(("localhost",5500))
serverSocket.listen()
while True:
    print("Server is listening at port 5500")
    clientSocket,clientSocketName=serverSocket.accept()
    t=MyThread(serverSocket,clientSocket)
    t.start()
serverSocket.close()