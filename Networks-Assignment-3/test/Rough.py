import argparse
import socket
import time
import datetime
import threading

MAX_SIZE_BYTES = 65535 # Mazimum size of a UDP datagram

# Delimiter
delimiter = "|"

# Set address and port
serverAddress = "localhost"
serverPort = 10000

'''
Application Layer Protocol which adds reliability function for UDP in socket class python.
Use ../resources/Thesis.pdf for reference
'''
# Packet class definition
class packet():
    checksum = 0
    length = 0
    seqNo = 0
    msg = 0
    
    def make(self, data):
        self.msg = data
        self.length = str(len(data))
        self.checksum=checksum(data)
        print ("Length: %s\nSequence number: %s" % (self.length, self.seqNo))

#Ack generation
ack=None
def ack_gen(socket):
    try:
        ack,serveraddress = recvfrom(MAX_SIZE_BYTES)
    except:
        ack=None

   

# checksum functions needed for calculation checksum
def checksum(msg):
    s = 0

    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
        s = s + w

    s = (s>>16) + (s & 0xffff)
    s = s + (s >> 16)

    #complement and mask to 4 byte short
    s = ~s & 0xffff

    return s

    
def send(data):
    time_limit = 2
    # Fragment and send file 500 byte by 500 byte
    x = 0
    pkt=packet()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#use our Rudp Sockets
    
    while x < (len(data) / 100) + 1:#decrease 1
       # packet_count += 1
        msg = data[x * 100 : x * 100 + 100]#out of bounds
        pkt.make(msg)
        finalPacket = str(pkt.checksum) + delimiter + str(pkt.seqNo) + delimiter + str(pkt.length) + delimiter + pkt.msg
        flag=0

        while True:
            if(flag==1):# use a flag TIMEDOUT
                break
            start_time= time.time()
            sock.sendto(finalPacket ,serverAddress)

            #Creating a thread to calculate acknowledgement 
            ackthread = threading.Thread(target = ack_gen, args = (sock,))
            ackthread.start()

            while(abs(time.time() - start_time) < time_limit):
                #ack is not yet received
                if(ack==None):
                    continue
                #ack received
                if(ack == pkt.seqNo):
                    #toggling the sequence number if the packet has reached properly
                    pkt.seqNo = int(not pkt.seqNo)
                    flag=1
                    #initialising ack
                    ack=None
                    break

                if( ack != pkt.seqNo):
                    break

            ackthread.join()

def receive(self):
    expected_seq_num = 0
    last =0
    while last==0:
        try:
            data, clientAddress = self.recvfrom(MAX_SIZE_BYTES)
            data = data.decode('ascii')
            pkt = packet()
            
        except:
            continue

        if checksum(message.split("|")[3]) != "1111111111111111" :
            #final=str(not expected_seq_num)+ "|ACK"
            pkt.make()
            finalPacket = str(pkt.checksum) + delimiter + str(not expected_seq_num) + delimiter + str(pkt.length) + delimiter +pkt.last+delimiter+ pkt.msg        
            self.ourSocket.sendto(finalPacket, serverAddress )                   
    
        elif expected_seq_num != str(data.split("|")[1]):
                data=str(not expected_seq_num)+"|ACK"
                pkt.make(data)

        elif expected_seq_num == str(data.split("|")[1]):
                data=str(expected_seq_num)+",ACK"
                pkt.make(data)
                expected_seq_num = not expected_seq_num
    
    # TODO: check if rcv_sqno is same as sequence no of message
    # and send appropriate ack                


if __name__ == "__main__":
    send("Hi This is a big message")






                    

    
                









