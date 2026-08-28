import socket
import PySimpleGUI as sg
import sys
import random
import threading
import os
import library.server as server

launcher_ready = threading.Event()

def launcher_server(port):
    param_table = {
        b"\x01": None
    }
    #creating socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", port))
    #creating id
    id = random.randbytes(1)
    #testing connection
    server.send_message(server.proto_1, id, b"\x55", client)

    data = server.get_message(client, 5)
    main_id, message = server.check_validity(data, server.proto_1, None, client)
    if message != b"\xAA":
        client.close()
        raise Exception("Received an incorrect test message. Transmission is not trustworthy.")
    #sending test result
    server.send_message(server.proto_2, id, b"\x00\x01", client)
    #getting acknowledgment
    data = server.get_message(client, 6)
    message = server.check_validity(data, server.proto_2, main_id, client)
    if message != b"\x00\x02":
        client.close()
        raise server.MOCRTransmissionProtocolError("", "message", message, b"\x00\x02")

    print("Received acknowledgment of handshake, ready to get info")
    server.send_message(server.proto_2, id, b"\x00\x03", client)
    #getting launcher parameters
    while message[0:1] != b"\x01":
        data = server.get_message(client, 6)
        message = server.check_validity(data, server.proto_2, main_id, client)

    key = message[1:2]
    parameter = param_table[key]
    server.send_message(server.proto_2, id, b"\x00\x02", client)

    data = server.get_message(client, 6)
    message = server.check_validity(data, server.proto_2, main_id, client)
    if message != b"\xFF\xFF":
        client.close()
        raise Exception("Fatal error: Socket connection not properly closed on main side.")
    return parameter

def launcher(param):
    consoles = [[sg.Checkbox("BOOSTER", key="-BOOSTER-"), sg.Checkbox("TELMU", key="-TELMU-")],
                [sg.Checkbox("RETRO", key="-RETRO-"), sg.Checkbox("CONTROL", key="-CONTROL-")],
                [sg.Checkbox("FDO", key="-FDO-"), sg.Checkbox("INCO", key="-INCO-")],
                [sg.Checkbox("GUIDO", key="-GUIDO-"), sg.Checkbox("FLIGHT", key="-FLIGHT-")],
                [sg.Checkbox("SURGEON",key="-SURGEON-"), sg.Checkbox("CAPCOM", key="-CAPCOM-")],
                [sg.Checkbox("EECOM", key="-EECOM-"), sg.Checkbox("GNC", key="-GNC-")]]
    layout = [[sg.Input(default_text='Name', key='-NAME-')],
              [sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse()],
            [sg.Listbox(values=[], enable_events=True, size=(40,20),key='-FILE LIST-')],
            [sg.Frame("Consoles", consoles)],
            [sg.Button("Start"), sg.Quit()]]
    window = sg.Window('Launcher', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if event == '-FOLDER-':                     # Folder name was filled in, make a list of files in the folder
            folder = values['-FOLDER-']
            try:
                file_list = os.listdir(folder)         # get list of files in folder
            except:
                file_list = []

            fnames = [f for f in file_list if os.path.isfile(
                os.path.join(folder, f)) and f.lower().endswith((".mismocr"))]
            window['-FILE LIST-'].update(fnames)  
        if event == '-START-':
            console_lst = []
            for items in consoles:
                console_lst.append(consoles[items].get)
            mission = window['-FILE LIST-']
            break
    return console_lst, mission

        
            


if __name__ == "__main__":
    #port = int(sys.argv[1])
    #launcher_server(port)
    launcher(None)
