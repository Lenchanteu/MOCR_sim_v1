import socket
import PySimpleGUI
import sys
import random
import threading
import engine.library.server as server

port = int(sys.argv[1])
launcher_ready = threading.Event()

def launcher_server(port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", port))

    #packet
    start = b"\x03"
    type = b"\x01"
    launch_id = random.randbytes(1)
    message = b"\x55"
    end = b"\x00"
    data = start + type + launch_id + message + end
    client.sendall(data)
    data = b""
    while len(data) < 5:
        buffer = client.recv(5 - len(data))
        data += buffer

    id, type, message = server.check_validity(data, [slice(0,1), slice(1,2), slice(2,3), slice(3,4), slice(4,5)], None, b"\x01", client)
    if message != b"\xAA":
        client.close()
        raise Exception("Received an incorrect test message. Transmission is not trustworthy.")

    start = b"\x03"
    type = b"\x02"
    message = b"\x00\x01"
    end = b"\x00"
    data = start + type + launch_id + message + end
    client.sendall(data)

    data = b""
    while len(data) < 6:
        buffer = client.recv(6 - len(data))
        data += buffer

    start = 
    

if __name__ == "__main__":
    launcher_server(port)
