import telemetry_rcv
class console():
    def __init__(self):
        self.telemetry = telemetry_rcv.global_telem

    #global telemetry loader for individual consoles. See documentation for telemetry format
    def load_telemetry(self, console_telem):
        