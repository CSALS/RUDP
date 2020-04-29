import argparse
import socket

MAX_SIZE_BYTES = 65535 # Mazimum size of a UDP datagram
my_ip = '127.0.0.1'
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((my_ip, 0))
print(f"RECEIVE\nListening at {s.getsockname()} For Receiving Messages\n")
print("------------------------------------------\n")
try:
    data, client_addr = s.recvfrom(MAX_SIZE_BYTES)
except:
    print("not recvd")