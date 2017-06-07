

class BluetoothClient:
    """
    Base class that must be subclassed due to platform specific bluetooth implementations
    """
    def __init__(self):
        self.socket = None

    def scan(self):
        raise NotImplementedError

    def send(self, data):
        raise NotImplementedError

    def recv(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

