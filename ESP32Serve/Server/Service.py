'''
Created on Sep. 10, 2020


@author: Phil
'''
import socketserver as SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    # this is the function that will be called when the
    # socket recieves a message; the "self" object
    # passed to it as a parameter will contain all 
    # the properties and methods of the calling class
    #
    # it is the nature of the "TCPServer" to call
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

# python will look for a function named "main" as it's starting point.
# the below is a cheat, that doesn't define a function named "main"...
# instead it runs that code if the interpreter is busy looking for a function
# named "main"
if __name__ == "__main__":
    # HOST, PORT = "10.0.0.29", 9999
    HOST, PORT = "192.168.1.24", 9999
    # Create the server, binding to localhost on port 9999
    # we also give it the "MyTCPHandler" object defined above,
    # whch has been defined as a "BaseRequestHandler" object.
    # when the TCPServer method enumerates it below as the handler,
    # it will trigger it's built-in call to a "handle" method and 
    # feed it an object that satisfies the parameter requirement to construct
    # the "MyTCPHandler" object (aka an object of the type "BaseRequestHandler") 
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()