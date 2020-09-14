'''
Created on Sep. 14, 2020

@author: Phil
'''

import socketserver as SocketServer


class Handler(SocketServer.BaseRequestHandler):
        
    """
    The request handler class for our server.  It defines "self" 
    as a SocketServer.BaseRequestHandler (aka "extends the class").
    It is instantiated (ie used as a template to make an object)
    once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

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
        print (self.data)
        # just send back the same data to the client, but upper-cased
        self.request.sendall(self.data.upper())
