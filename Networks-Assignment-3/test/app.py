import threading
from threading import Thread
import argparse, socket
import rudp
import os

MAX_SIZE_BYTES = 65535 # Max Size of UDP datagram

my_ip = '127.0.0.1' # Default IP To Receive Message

import logging

# Receiving Messages
def runner():
    try:
        print("eternal running")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((my_ip, 0))
        s.setblocking(0)
        data, client_addr = s.recvfrom(MAX_SIZE_BYTES)
    except:
        f= open("error.log","w+")
        f.write("error")
        f.close()

if __name__ == "__main__":
    k = 0
    while k < 3:
        k = k + 1
        print(f"Start {k} iteration")
        kill_thread = True
        ackthread = threading.Thread(target = runner)
        ackthread.start()
        i = 0
        while i < 10:
            print("i ",i)
            i = i + 1

        if kill_thread == True:
            print(f"In {k} iteration, killing thread")
            ackthread._stop()
            print(f"In {k} iteration, killed the thread")
        else:
            ackthread.join()

        print(f"End {k} iteration")

    print("Done")
        



