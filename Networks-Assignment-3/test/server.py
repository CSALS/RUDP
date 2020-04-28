import argparse, socket
from rudp import rudp
MAX_SIZE_BYTES = 65535 # Mazimum size of a UDP datagram


import timeit # To measure time for code snippet to execute

def server(port):
    s = rudp(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = '127.0.0.1'
    s.bind((hostname, port))
    print('Listening at {}'.format(s.getsockname()))
    while True:
        start = timeit.timeit()
        data, clientAddress = s.read()
        end = timeit.timeit()
        print(end - start) # Time elapsed
        message = data.decode('ascii')
        print('The client at {} says {!r}'.format(clientAddress, message))
        # msg_to_send = input('Input message to send to client:' )
        # data = msg_to_send.encode('ascii')
        # s.sendto(data, clientAddress)

if __name__ == "__main__":
    server(4001)
