#This is the library for all server operations

import socket
proto_1 = {"prt" : [slice(0,1), slice(1,2), slice(2,3), slice(3,4), slice(4,5)], "num" : b"\x01"}
proto_2 = {"prt" : [slice(0,1), slice(1,2), slice(2,3), slice(3,5), slice(5,6)], "num" : b"\x02"}
class MOCRTransmissionProtocolError(Exception):
    """Error raised when an error on a malfunction of the custom socket transmission protocol"""
    def __init__(self, message, step, received, expected):
        self.message = message
        self.step = step
        self.received = received
        self.expected = expected
        super().__init__(message)

    def __str__(self):
        return f"MOCR transmission protocol error: {self.message} The error occured because the {self.step} was not correct. Received {self.received}, but {self.expected} was expected."
    
def check_validity(data, byte_order, id, conn):
    """Checks data validity of a MOCR protocol based transmission. Returns message or if id=None, returns id, message"""
    start = data[byte_order["prt"][0]]
    ctype = data[byte_order["prt"][1]]
    cid = bytes(data[byte_order["prt"][2]])
    message = bytes(data[byte_order["prt"][3]])
    end = data[byte_order["prt"][4]]
    type = byte_order["num"]
    byte_order = byte_order["prt"]
    if start != b"\x03":
        conn.close()
        raise MOCRTransmissionProtocolError("", "start", start, b"\x03")
    
    if end != b"\x00":
        conn.close()
        raise MOCRTransmissionProtocolError("", "end", end, b"\x00")
    if ctype != type:
        conn.close()
        raise MOCRTransmissionProtocolError("", "type", ctype, type)
    if id != None:
        if cid != id:
            conn.close()
            raise MOCRTransmissionProtocolError("", "id", cid, id)
    elif id == None:
        return cid, message
    return message
def get_message(conn, length):
    data = b""
    while len(data) < length:
        buffer = conn.recv()
        data += buffer
    return data
def send_message(protocol, id, message, conn):
    start = b"\x03"
    ttype = protocol["num"]
    end = b"\x00"
    data = start + ttype + id + message + end
    conn.sendall(data)
    return 0

    