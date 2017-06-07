# file: rfcomm-client.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a client application that uses RFCOMM sockets
#       intended for use with rfcomm-server
#
# $Id: rfcomm-client.py 424 2006-08-24 03:35:54Z albert $

from app.btclient import BluetoothClient
from bluetooth import *
import sys
import time


class BluetoothClientPC(BluetoothClient):
    def __init__(self, addr=None):
        super().__init__()

        self.port = None
        self.name = None
        self.host = None

        self.scan(addr=addr)

    def scan(self, addr=None):
        # search for the SampleServer service
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        service_matches = find_service(uuid=uuid, address=addr)

        if len(service_matches) == 0:
            print("couldn't find the SampleServer service =(")
        else:
            first_match = service_matches[0]
            self.port = first_match["port"]
            self.name = first_match["name"]
            self.host = first_match["host"]

        print("connecting to \"%s\" on %s" % (self.name, self.host))

        # Create the client socket
        self.socket = BluetoothSocket(RFCOMM)
        self.socket.connect((self.host, self.port))

    def send(self, data):
        if data:
            self.socket.send(data)

    def recv(self):
        raise NotImplementedError

    def disconnect(self):
        self.socket.close()


if __name__ == '__main__':
    """
    Test bluetooth client
    """
    addr = None

    if len(sys.argv) < 2:
        print("no device specified.  Searching all nearby bluetooth devices for")
        print("the SampleServer service")
    else:
        addr = sys.argv[1]
        print("Searching for SampleServer on %s" % addr)

        bt_pc = BluetoothClientPC(addr=addr)  # will block until a connection is made

        while True:
            try:
                bt_pc.send("test-data")  # send a string to the server
                time.sleep(1)

            except (KeyboardInterrupt, SystemExit):
                sys.exit(0)
