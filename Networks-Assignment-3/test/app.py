import threading
import argparse, socket
import rudp

MAX_SIZE_BYTES = 65535 # Max Size of UDP datagram

my_ip = '127.0.0.1' # Default IP To Receive Message

# Receiving Messages
def server(s):
    # my_ip = '127.0.0.1'
    while True:
        data, client_addr = s.recvfrom(MAX_SIZE_BYTES)
        message = data.decode('ascii')
        print(f"\nFrom client {client_addr} : {message}\nSend:", end=" ")

# Sending Messages
def client():
    s = rudp.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        dest_ip, dest_port, message = input("Send: ").split(',', 3)
        dest_port = int(dest_port)
        s.connect((dest_ip, dest_port))
        data = message.encode('ascii')
        s.write(data)

if __name__ == "__main__":
    # Helper Stuff
    # my_ip = input("Enter Your Local IP On Which You Want To Receive\n")
    print("\n\nTO SEND\nFormat To Send A Message To Anyone:\n \
    [destination_ip destination_port message to be sent]\n \
        With Comma Between Them And No Space Between Them.\n \
    Example :-\n \
        127.0.0.1,4000,Hello Bro How Are You Doing \n\n")

    # Creating Sockets
    s = rudp.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((my_ip, 0))
    print(f"RECEIVE\nListening at {s.getsockname()} For Receiving Messages\n")
    print("------------------------------------------\n")

    # Create threads
    writing = threading.Thread(target=client)
    reading = threading.Thread(target=server, args=(s,))

    # Start threads
    writing.start()
    reading.start()

    # Wait till threads are completed
    writing.join()
    reading.join()

    # Both threads are done
    print("Done")
