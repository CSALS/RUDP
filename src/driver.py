import threading
import argparse, socket
from rudp import Rudp
import sys,os
import signal
import time

MY_IP = '127.0.0.1' # Default IP To Receive Message

# Receiving Messages
def server():
    i=0
    try:
        while True:
	    # Creating Socket
            s = Rudp() #socket creation
            s.bind(MY_IP)
            print(f"RECEIVE\nListening at {s.ourSocket.getsockname()} For Receiving Messages\n")
            print("------------------------------------------\n")
            data, client_addr = s.read()
            #print("inserver")
            #print(data)
            #message = data.decode('ascii')#Unnecessary decode
            print(f"\nFrom client {client_addr} : {data}\n")
            del s
            time.sleep(2.5)
    except (KeyboardInterrupt, SystemExit):
        os._exit(0)

# Sending Messages
def client():
    i=0
    try:
        while True:
            s = Rudp()
            dest_ip = MY_IP
            dest_port, message = input("Send: ").split(',', 2)
            dest_port = int(dest_port)
            s.connect(dest_ip, dest_port)
            data = message.encode('ascii')#Unnecessary encode
            s.write(data)
            del s
            time.sleep(2.5)
    except (KeyboardInterrupt, SystemExit, EOFError, ValueError):
        os._exit(0)
        

if __name__ == "__main__":
    # Helper Stuff
    # MY_IP = input("Enter Your Local IP On Which You Want To Receive\n")
    print("\n\nTO SEND\nFormat To Send A Message To Anyone:\n \
    [destination_port,message to be sent]\n \
        With Comma Between Them And No Space Between Them.\n \
    Example :-\n \
	4000,Hello Bro How Are You Doing \n\n \
    Press Ctrl + C / Cmd + C to Exit the application \n\n")

    
    # Create threads
    writing = threading.Thread(target=client)
    reading = threading.Thread(target=server)


    # Start threads
    writing.start()
    reading.start()
    try:
        # Wait till threads are completed
        writing.join()
        reading.join()

        # Both threads are done
        print("Done")
    except KeyboardInterrupt:
        os._exit(0)
