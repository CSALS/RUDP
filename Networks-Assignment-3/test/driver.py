import threading
import argparse, socket
from rudp import Rudp
import sys,os
import signal

MY_IP = '127.0.0.1' # Default IP To Receive Message

# Receiving Messages
def server(s):
    i=0
    try:
        while True:
            data, client_addr = s.read() ######CRITICAL######### need to invoke rudp recv method here
            #print("inserver")
            #print(data)
            #message = data.decode('ascii')#Unnecessary decode
            print(f"\nFrom client {client_addr} : {data}\nSend: ",end="")
    except (KeyboardInterrupt, SystemExit):
        os._exit(0)

# Sending Messages
def client():
    s = Rudp()
    i=0
    try:
        while True:
            dest_ip = MY_IP
            dest_port, message = input("Send: ").split(',', 2)
            dest_port = int(dest_port)
            s.connect(dest_ip, dest_port)
            data = message.encode('ascii')#Unnecessary encode
            s.write(data) #####CRITICAL######## need to invoke our rudp send method
    except (KeyboardInterrupt, SystemExit, EOFError, ValueError):
        os._exit(0)
        

if __name__ == "__main__":
    # Helper Stuff
    # MY_IP = input("Enter Your Local IP On Which You Want To Receive\n")
    print("\n\nTO SEND\nFormat To Send A Message To Anyone:\n \
    [destination_ip destination_port message to be sent]\n \
        With Comma Between Them And No Space Between Them.\n \
    Example :-\n \
        127.0.0.1,4000,Hello Bro How Are You Doing \n\n \
    Press Ctrl + C / Cmd + C to Exit the application \n\n")

    # Creating Sockets
    s = Rudp()#socket creation
    s.bind(MY_IP)
    print(f"RECEIVE\nListening at {s.ourSocket.getsockname()} For Receiving Messages\n")
    print("------------------------------------------\n")

    # Create threads
    writing = threading.Thread(target=client)
    reading = threading.Thread(target=server, args=(s,))


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
