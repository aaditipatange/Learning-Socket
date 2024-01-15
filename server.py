import socket
import threading

#Global Constants
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(ADDR)

def handle_client(conn, addr):
    """
    Handles communication with a single client. This function is designed to be called in a separate thread
    so that the server can manage multiple clients simultaneously.
    Parameters: conn
    The TCP socket object representing the connection to the client.
    Parameters: addr
    A tuple containing the IP address and port number of the client.
    Return: None
    """
    print(f"[New Connection] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
    conn.close()


def start():
    """
    Starts the server by setting up the listening socket and starting a new thread for each incoming connection
    Return: None
    """
    Server.listen()
    print(f"[Listening] Server is listening on {Server}")
    while True:
        conn, addr = Server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[Active Connections] {threading.activeCount()-1}")

print("[Starting] Server is up and running...")
start()
