import socket 
import threading


class client:
    client_socket = None

    def __init__(self):
        
        self.initialize_socket()
        
    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        remote_ip = '127.0.0.1'
        remote_port = 10319 
        print(" request connection to the server")
        self.client_socket.connect((remote_ip, remote_port))
        self.data="connection made with the client"
        self.client_socket.send(self.data.encode())
        self.dataFromServer=self.client_socket.recv(1024)
        print(self.dataFromServer.decode())
    
    
    
#main function    
if __name__ == '__main__':
   client()
   
