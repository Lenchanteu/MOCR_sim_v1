#Main.py
#Main file
#
# Code starts here:

#------------------IMPORTS------------------------
import PySimpleGUI as sg
import threading
import subprocess
import socket
import math
import sys
from pathlib import Path
import engine.library.server as server
#------------------LAUNCHER------------------
#threading event definitions
launcher_ready = threading.Event()
server_connected = threading.Event()
#call Launcher
project_dir = Path(__file__).resolve().parent
def server_launcher(param="None"):
    #variables
    data = b""
    param_table = {
        "None": b"\x01"
    }
    param_message
    server_co = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_co.bind(("127.0.0.1", 0))
    server_co.listen(10)

    port = server_co.getsockname()[1]
    subprocess.Popen(
        [sys.executable, r"engine/launcher.py", str(port)], cwd=project_dir
    )
    conn, addr = server_co.accept()
    server_connected.set()

    data = server.get_message(conn, 5)
    #decode test data:
    id_launcher, message = server.check_validity(data, server.proto_1, None, conn)
    if message != b"\x55":     
        conn.close()
        raise server.MOCRTransmissionProtocolError("", "message", message, b"\x55")
    #compose test message:
    id = bytes([(id_launcher[0] + 1) & 0xFF])

    server.send_message(server.proto_1, id, b"\xAA", conn)
    
    data = server.get_message(conn, 6)
    # decode data
    message = server.check_validity(data, server.proto_2, id_launcher, conn)
    if message != b"\x00\x01":
        conn.close()
        raise Exception(f"Unexpected message received: {message}")
    
    server.send_message(server.proto_2, id, b"\x00\x02", conn)


    
    message = None
    while message != b"\x00\x03":
        data = server.get_message(conn, 6)
        message = server.check_validity(data, server.proto_2, id_launcher, conn)

        server.send_message(server.proto_2, id, b"\x00\x02", conn)
        if message == b"\xAA\xAA":
            conn.close()
            raise Exception("A fatal error occured. No more info")
        data = server.get_message(conn, 6)
    message = b"\x01" + param_table[param] 
    server.send_message(server.proto_2, id, message, conn)

    data = server.get_message(conn, 6)
    message = server.check_validity(data, server.proto_2, id_launcher, conn)
    if message == b"\xAA\xAA":
        conn.close()
        raise Exception("A fatal error occured. No more info")
    elif message != b"\x00\x02":
        conn.close()
        raise Exception(f"Unexpected message received: {message}")

    server.send_message(server.proto_2, id, b"\xFF\xFF", conn)
    launcher_ready.set()
    print("launcher launched")
    conn.close()
    quit(0)
            
def launch(param):
    available_param = ["None"]
    if param not in available_param:
        raise Exception("Parameter %(param)s not available. Please restart with correct arguments" % {
            "param": param
        })
    layout = [[sg.Text("Getting everything ready", text_color="green", background_color="black")],
        [sg.Graph(
            canvas_size=(100, 100),
            graph_bottom_left=(0,0),
            graph_top_right=(100,100),
            background_color="black",
            key="-GRAPH-"
        )]
    ]
    window = sg.Window("Spinner", layout, finalize=True, background_color="black")
    angle = 0
    arc_length = 1
    arc_decorinc = True
    server_thread = threading.Thread(target=server_launcher, args=(param,))
    server_thread.start()
    while True:
        event, values = window.read(timeout=50)

        if event == sg.WIN_CLOSED:
            break
        graph = window["-GRAPH-"]
        graph.erase()

        cx, cy = 50,50
        radius = 30

        
        segments = 40

        for i in range(segments):
            a1 = math.radians(angle + i * arc_length / segments)
            a2 = math.radians(angle + (i + 1) * arc_length / segments)

            x1 = cx + math.cos(a1) * radius
            y1 = cy + math.sin(a1) * radius

            x2 = cx + math.cos(a2) * radius
            y2 = cy + math.sin(a2) * radius

            graph.draw_line(
                (x1,y1),
                (x2,y2),
                width=5,
                color="green"
            )
            
        if arc_decorinc:
            arc_length += 5
            angle = (angle + 10) % 360
        else:
            arc_length -= 5
            angle = (angle + 15) % 360
        if arc_length > 270:
            arc_decorinc = False 
        if arc_length < 0:
            arc_decorinc = True 
        
    window.close()

if __name__ == "__main__":
    launch("None")