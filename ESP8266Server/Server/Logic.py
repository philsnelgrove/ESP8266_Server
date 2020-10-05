'''
Created on Sep. 14, 2020

@author: Phil
'''

import socketserver as SocketServer
import socket
import ESP8266Server.Server.Data as Data
import json


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
    mac_address = 'null'
    operation = 'null'
    request_data = 'null'

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
        if (self.datasource.node_lookup_id_by_mac(self.mac_address) == 0):
            print("unauthorized contact")
            return()
        self.respond()

    def check_for_handshake(self):
        # process parsed response for handshake info
        if (self.operation == "register_client"):
            print('client registration request found')
            print('mac address is {}'.format(self.mac_address))
            check_for_client = self.datasource.node_lookup_id_by_mac(self.mac_address)
            if (check_for_client == 0):
                insert_result = self.datasource.register_node("NewNode", self.mac_address, str(self.client_address[0]))
                return(insert_result)
            else:
                return("client already registered")
            # return(insert_result)
            return("registered")
        else:
            # print('not a registration attempt')
            return("no registration required")

    def parse_data(self):
        request_object = json.loads(self.data)
        self.mac_address = request_object['mac']
        self.operation = request_object['operation']
        self.request_data = request_object['data']
        print("request processed")

    def respond(self):
        # just send back the same data to the client, but upper-cased
        response = str.upper('*** ' + self.operation + ' complete')
        self.request.sendall(str.encode(response))


def send_command_to_node(self, ip, port, command, data="null"):
    # this will send a command to a node.
    # this function doesn't care what
    # the command is or which node
    # it sends to, that is established
    # when the call is made, and passed
    # in the parameters.  This allows us
    # to send any command to any node.
    #
    # form an object for our message
    object_to_form = {
        "command": command,
        "data": data,
    }
    # serialize the object into a
    # JSON string
    json_message = json.dumps(object_to_form)
    # print it out for good measure...
    # this is debug and TBR
    print(json_message)
    # set up the criteria to open
    # a socket with the node, seding
    # our message
    TCP_IP = ip
    TCP_PORT = port
    BUFFER_SIZE = 1024
    MESSAGE = json_message
    # establish the socket using our config
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the configured socket
    s.connect((TCP_IP, TCP_PORT))
    # send our message
    s.send(MESSAGE.encode())
    # recieve feedback
    #  data = s.recv(BUFFER_SIZE)
    # close connection
    s.close()
    # print out the response from the node
    print("received data:", data)
