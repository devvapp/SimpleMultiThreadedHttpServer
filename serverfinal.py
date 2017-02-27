import socket
from threading import Thread
import sys, getopt, os.path
from urlparse import urlsplit

class ServerThread(Thread):

    def __init__(self, ip, port, isocket):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket= isocket

    def get_file_contents(self, file_path):
        response_data=""
        my_file = os.path.isfile(file_path)
        if my_file:
            with open(file_path) as f:
                content = "\n".join(f.readlines())
                response_data = "HTTP/1.0 200 OK\nContent-Type: text/html; charset=utf-8\nContent-Length: "+str(len(content))
                response_data += "\n\n"
                response_data += content
        if not my_file :
            response_data = "HTTP/1.1 404 Not Found\nContent-Type: text/html;"
            #response_data += "\n\n404 Not Found"

        return response_data

    def relpath(self, path):
        return path.strip('/') 

    def parse_preamble(self, body):
        line1 = body.split('\n')[0]
        method, path, httpversion = line1.split(' ')
        return method, path, httpversion

    def run(self):
        clientData = self.socket.recv(4096)
        
        method, path, httpversion = self.parse_preamble(clientData)
        fpath = self.relpath(path)
        res_str = self.get_file_contents(fpath)
        self.socket.send(res_str)  # echo
        self.socket.close()


def run( port ):
    threads = []
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(('localhost', port))
    serverSocket.listen(5)
    while True:
        (clientSocket, (clientIP, clientPort)) = serverSocket.accept()
        newServerThread = ServerThread(clientIP, clientPort, clientSocket)
        newServerThread.start()
        threads.append(newServerThread)

    for serverThread in threads:
        serverThread.join()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Usage : serverfinal.py <port_number>")
    port = int(sys.argv[1])
    run(port)
