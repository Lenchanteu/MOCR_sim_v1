#This is the library for all server operations

import socket

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
    
def check_validity(data, byte_order, id, type, conn):
    start = data[byte_order[0]]
    ctype = data[byte_order[1]]
    cid = data[byte_order[2]]
    message = data[byte_order[3]]
    end = data[byte_order[4]]
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
        return cid, ctype, message
    return ctype, message


    