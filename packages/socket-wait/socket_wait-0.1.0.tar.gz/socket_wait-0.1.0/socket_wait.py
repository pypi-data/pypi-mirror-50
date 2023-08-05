"""
socket_wait will block execution, listening on the provided socket until a connection is received.
It will then exit, without processing the data sent. It mostly provides a simple way for one process to call back to
another.
"""
from __future__ import print_function

import socket
import sys

__version__ = '0.1.0'


def wait(listen_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(('0.0.0.0', listen_port))
        except OSError:
            print("Port is already in use.")
            sys.exit(1)

        sock.listen()
        conn, addr = sock.accept()
        with conn:
            print("connected by", ':'.join(map(str, addr)) + '.', 'exiting...')


def cli():
    if len(sys.argv) != 2:
        print("Usage: socket_wait PORT")
        sys.exit(0)

    try:
        listen_port = int(sys.argv[1])
    except ValueError:
        print("Must provide an integer port.")
        sys.exit(1)

    if listen_port <= 1023:
        print("Must provide a port >= 1024.")
        sys.exit(1)

    try:
        wait(listen_port)
    except KeyboardInterrupt:
        print("Exiting without a connection.")
