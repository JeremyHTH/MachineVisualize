import socket, yaml
import threading

HOST = "127.0.0.1" #socket.gethostname() #"127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 9086  # Port to listen on (non-privileged ports are > 1023)

def ConnectionHandler_YAML(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        while(data := conn.recv(1024).decode()):
            # print("Entered")
            print(data)
            Pos = yaml.safe_load(data)
            print(Pos)
            conn.send(b"Received")
        print("Disconnect")

def ConnectionHandler_JSON(conn, addr):
    print(f'Connected {addr}')
    with conn:
        while(data := conn.recv(1024).decode()):
            conn.send(b'Received')
        print("Disconnect")

def StartServer():
    Continue = True
    ThreadList = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while Continue:
            conn, addr = s.accept()
            NewThread = threading.Thread(target=ConnectionHandler_YAML, args=(conn, addr))
            # print(f"Connected by {addr}")
            # with conn:
            #     while(data := conn.recv(1024).decode()):
            #         # print("Entered")
            #         Pos = yaml.safe_load(data)
            #         print(Pos)
            #         conn.send(b"Received")

            #     print("Disconnect")
            NewThread.start()
    
    for Thread in ThreadList:
        Thread.join()

def StartUDPServer():
    Continue = True
    ThreadList = []
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        # s.listen()
        while Continue:
            # conn, addr = s.accept()
            # NewThread = threading.Thread(target=ConnectionHandler_YAML, args=(conn, addr))
            # print(f"Connected by {addr}")
            # with conn:
            #     while(data := conn.recv(1024).decode()):
            #         # print("Entered")
            #         Pos = yaml.safe_load(data)
            #         print(Pos)
            #         conn.send(b"Received")

            #     print("Disconnect")
            # NewThread.start()
            print("Entered")
            Message, Address = s.recvfrom(1024)
            print(Message.decode())

if __name__ == '__main__':
    StartUDPServer()