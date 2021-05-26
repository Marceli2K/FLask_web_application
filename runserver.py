"""
This script runs the SIOS_Eimpreza application using a development server.
"""

from os import environ
from SIOS_Eimpreza import app
import socket

if __name__ == '__main__':

    
    host_address=socket.gethostbyname(socket.gethostname())

    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(host_address, 55555)

