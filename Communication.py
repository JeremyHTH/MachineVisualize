import socket, yaml
import threading

HOST = socket.gethostname()#"127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 9086  # Port to listen on (non-privileged ports are > 1023)

def ConnectionHandler(conn, addr):
    print(f"Connected by {addr}")
    with conn:
        while(data := conn.recv(1024).decode()):
            # print("Entered")
            Pos = yaml.safe_load(data)
            print(Pos)
            conn.send(b"Received")
        print("Disconnect")

def StartServer():
    Continue = True
    ThreadList = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while Continue:
            conn, addr = s.accept()
            NewThread = threading.Thread(target=ConnectionHandler, args=(conn, addr))
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

if __name__ == '__main__':
    StartServer()