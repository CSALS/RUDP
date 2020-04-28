import argparse
import socket
from rudp import rudp

MAX_SIZE_BYTES = 65535 # Mazimum size of a UDP datagram

def client(port):
    s = rudp(socket.AF_INET, socket.SOCK_DGRAM)
    host = '127.0.0.1'
    while True:
        s.connect((host, port))
        message = input('Input message to send to server:' )
        data = message.encode('ascii')
        # Now our rudp class will take care of sending the data to the destination for sure.
        s.write(data)

client(4001)
