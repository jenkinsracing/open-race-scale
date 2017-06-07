# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *


class BluetoothServer:
    """
    CURRENTLY FOR TESTING ONLY
    """
    def __init__(self):
        self.server_socket = BluetoothSocket(RFCOMM)

        self.server_socket.bind(("", PORT_ANY))
        self.server_socket.listen(1)
        self.port = self.server_socket.getsockname()[1]

        self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        self.client_socket = None
        self.client_info = None

        self.advertise()

    def advertise(self):
        advertise_service(self.server_socket, "orctest",
                          service_id=self.uuid,
                          service_classes=[self.uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE],
                          # protocols = [ OBEX_UUID ]
                          )

        print("Waiting for connection on RFCOMM channel %d" % self.port)

        self.client_socket, self.client_info = self.server_socket.accept()
        print("Accepted connection from ", self.client_info)

    def send(self, data):
        if data:
            self.client_socket.send(len(data))
            print('sent: ', data)

    def recv(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if len(data) == 0:
                    break
                print("received [%s]" % data)
        except IOError:
            pass

        self.disconnect()

    def disconnect(self):
        print("disconnected")

        self.client_socket.close()
        self.server_socket.close()
        print("all done")
