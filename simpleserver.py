import sys
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

Handler = SimpleHTTPRequestHandler
Server = BaseHTTPServer.HTTPServer
Protocol = 'HTTP/1.0'


def create_and_serve(address=None, port=None):
    """ Create  a HTTP server at 127.0.0.1 and the specified port
    Default to port 8000 is a port is not specified
    """
    port = 8000 if port is None else int(port)
    address = '127.0.0.1' if address is None else str(address)

    serve_to = (address, port)

    Handler.protocol_version = Protocol
    httpd = Server(serve_to, Handler)

    socks = httpd.socket.getsockname()
    print("Grab a napkin and get served on {} port {}".format(socks[0], socks[1]))
    httpd.serve_forever()
    return "{}:{}".format(address, port)
