'''
Created on Sep. 14, 2020

@author: Phil
'''

import socketserver as SocketServer
import ESP8266Server.Server.Data as Data


class Handler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.  It defines "self"
    as a SocketServer.BaseRequestHandler (aka "extends the class").
    It is instantiated (ie used as a template to make an object)
    once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    datasource = Data.DataSource()

    # this is the class function (or "method") that will be called when the
    # socket recieves a message; the "self" object
    # passed to it as a parameter will contain all
    # the properties and methods of the parent class
    # (defined as SocketServer.BaseRequestHandler)
    #
    # it is the nature of the "SocketServer.TCPServer" (from "Service") to call
    # a method named "handle" off the object it's been given as a handler.
    # We override that method here, and this one gets called instead.
    def handle(self):
        print ("connection detected")
        # self.request is the TCP socket connected to the client
        # this line will "grab" the first 1024 bytes of data
        # off the request object and then remove all the trailing spaces
        self.data = self.request.recv(1024).strip()
        # these print to STDOUT information about the communication
        print ("{} wrote:".format(self.client_address[0]))
        self.parse_data()
        print("handshake check result is {}".format(self.check_for_handshake()))
        self.respond()

    def check_for_handshake(self):
        # process parsed respose for handshake info
        comparison = str(self.data[:4])
        print (comparison)
        if ("MAC:" in str(self.data)):
            print('mac address found')
            print('address is {}'.format(self.data[4:]))
            insert_result = self.datasource.register_node("NewNode", str(self.data[4:]), str(self.client_address[0]))
            return(insert_result)
        else:
            print('no mac address found')

    def parse_data(self):
        print (self.data)

    def respond(self):
        # just send back the same data to the client, but upper-cased
        self.request.sendall(self.data.upper())
