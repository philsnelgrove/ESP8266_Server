'''
Created on Sep. 10, 2020


@author: Phil
'''
# import the "socketserver" module from
# the python libraries, and our own
# "Logic" module which must be pathed to
import socketserver as SocketServer
import ESP8266Server.Server.Logic as Logic

# python will look for a function named "main" as it's starting point.
# the below is a cheat, that doesn't define a function named "main"...
# instead it runs that code if the interpreter is busy looking for a function
# named "main"
if __name__ == "__main__":
    # home
    HOST, PORT = "10.0.0.29", 9999
    # bear's
    # HOST, PORT = "192.168.1.26", 9999
    # Dustin's
    # HOST, PORT = "192.168.0.150", 9999
    
    # Create the server, binding to localhost on port 9999
    # we also give it the "Handler" class object
    # defined in the "Logic" module (Logic.Handler),
    # whch has been defined as a "BaseRequestHandler" object.
    # when the TCPServer method enumerates it below as the handler,
    # it will trigger it's built-in call to a "handle" method and
    # feed it an object that satisfies the parameter requirement to construct
    # the "Handler" object (aka an object of the type "BaseRequestHandler")
    server = SocketServer.TCPServer((HOST, PORT), Logic.Handler)
    # ##server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
