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
#------------------LAUNCHER------------------
#threading event definitions
launcher_ready = threading.Event()
#call Launcher
def server_launcher(param):
    #variables
    data = b""
    server_co = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_co.bind(("127.0.0.1", 0))
    server_co.listen(10)

    port = server_co.getsockname()[1]

    conn, addr = server_co.accept()
    server_connected = True
    while len(data) < 5:
        buffer = conn.recv(5 - len(data))
        data += buffer
    #decode test data:
    start = data[0:1]
    type = data[1:2]
    id_launcher = data[2:3]
    message = data[3:4]
    end = data[4:5]
    if start != b"\x03":
        conn.close()
        raise Exception("The start object in the transmission protocol was not correct.")
    if type != b"\x01":
        conn.close()
        raise Exception("Received the wrong message type.")
    if end != b"\x00":
        conn.close()
        raise Exception("The end object in the transmission protocol was not correct.")
    if message != b"\x55":
        conn.close()
        raise Exception("Received an incorrect test message. Transmission is not trustworthy.")
    #compose test message:
    start = b"\x03"
    type = b"\x01"
    id_main = bytes([(id_launcher[0] + 1) & 0xFF])
    message = b"\xAA"
    end = b"\x00"
    data = start + type + id_main + message + end
    conn.sendall(data)
    data = b"" #reset data
    #receive info message
    while len(data) < 6:
        buffer = conn.recv(6)
        data += buffer
    # decode data
    start = data[0:1]
    type = data[1:2]
    cid_launcher = data[2:3]
    message = data[3:5]
    end = data[5:6]
    if start != b"\x03":
        conn.close()
        raise Exception("The start object in the transmission protocol was not correct.")
    if type != b"\x02":
        conn.close()
        raise Exception("Received the wrong message type.")
    if end != b"\x00":
        conn.close()
        raise Exception("The end object in the transmission protocol was not correct.")
    if cid_launcher != id_launcher:
        conn.close()
        raise Exception("The launcher ID has been changed. Connection not trustworthy")
    if message == b"\x00\x01":
        print("Connection successful, ready to send info")
        start = b"\x03"
        type = b"\x02"
        if param == None:
            message = b"\x00\x02"
        end = b"\x00"
        data = start + type + id_main + message + end
        conn.sendall(data)
    else:
        conn.close()
        raise Exception(f"Unexpected message received: {message}")
    
    launcher_ready.set()
def launch(param):
    available_param = ["None"]
    if param not in available_param:
        raise Exception("Parameter %(param)s not available. Please restart with correct arguments" % {
            "param": param
        })
    param_table = {
        "None": None
    }
    param_func = param_table[param]
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
    server_thread = threading.Thread(target=server_launcher)
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
        if launcher_ready.is_set():
            if 
        

        
        

    window.close()

if __name__ == "__main__":
    launch("None")