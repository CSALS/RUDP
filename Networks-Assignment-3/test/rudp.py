import argparse
import socket
import time
import datetime
import threading

MAX_SIZE_BYTES = 65535 # Mazimum size of a UDP datagram

# Delimiter
delimiter = "|"


#TODO check if ack is corrupted sender
#TODO DONE data send in receive (buffer)
#TODO checksum
#TODO dynamic timeout
#TODO Can our code handle multiple clients and mult servers(self.acknowledgment)?


'''
Application Layer Protocol which adds reliability function for UDP in socket class python.
'''
# Packet class definition
class packet():
    
    def __init__(self,message=None):
        self.msg = message
        self.length = str(len(message))
        self.checksum=0
        self.last=0
        self.seqNo=0
    
def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


class Rudp():
    acknowledgment=None#CLASS VARIABLE WORKS ONLY IF SINGLE CLIENT SERVER
    
    # Socket Creation and Initialisation

    def __init__(self,sock=None): 
        if sock is None:
            self.ourSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.ourSocket = sock
    def bind(self,ipaddr):
        self.myip=ipaddr#SERVER IP 
        self.ourSocket.bind((ipaddr,0)) #Server is bound to udp socket with a random free port assigned

    def connect(self,host,port):
        self.toip=host
        self.toport=port
        self.ourSocket.connect((host,port))

    # Receive Acknowledgment   
                  
    def ack_gen(self,sock):
        try:
            self.acknowledgment,self.toaddress = sock.recvfrom(MAX_SIZE_BYTES)
            self.acknowledgment = self.acknowledgment.decode('ascii')
            # Gives the number of Acknowledgment packet
            self.acknowledgment=self.acknowledgment.split("|")[2]      
            print("ACK received == "+self.acknowledgment)

        except:
            self.acknowledgment=None

    # Sender Function           
    def write(self,data):
        gseqNo=0
        time_limit=2     
        sock = self.ourSocket
        
        # Fragment and send file in chunks of 3 byte 
        generator = chunkstring(data,3)
        list_of_packet_strings=list(generator)
                
        for i in range(0,len(list_of_packet_strings)):           
            
            # Each msg is a bstring i.e b'hello' or b'there'
            msg=list_of_packet_strings[i]       
            msg=msg.decode('ascii')

            # Packet Creation
            pkt=packet(msg)
            pkt.seqNo=gseqNo
          
            print("pkt Seq: " + str(pkt.seqNo))
            if(i==len(list_of_packet_strings)-1 ):     
                pkt.last=1

            finalPacket = str(pkt.seqNo) + delimiter + str(pkt.length) +delimiter+str(pkt.last)+ delimiter + (pkt.msg) # Will be put in payload
            pkt.checksum=self.checksum(finalPacket,0)
            finalPacket = str(pkt.checksum) + delimiter + str(pkt.seqNo) + delimiter + str(pkt.length) +delimiter+str(pkt.last)+ delimiter + (pkt.msg) # Will be put in payload
            encodedPacket =finalPacket.encode('ascii')

            first_iter=True # If first iteration of the message
            TIMED_OUT=False
            while TIMED_OUT or first_iter :
                TIMED_OUT=False
                first_iter=False
                start_time= time.time()
                sock.sendto(encodedPacket , (self.toip,self.toport))

                #Creating a thread to calculate acknowledgement 
                ackthread = threading.Thread(target = self.ack_gen, args = (sock,))
                ackthread.start()
                
                while(not TIMED_OUT): 

                    TIMED_OUT= not ( abs(time.time() - start_time) < time_limit)

                    #TODO CHECK CHECKSUM FOR ACK
                                     
                    # Ack is not yet received                                                                                                       
                    if(self.acknowledgment == None):
                        continue
                    
                    # Ack received
                    if(self.acknowledgment== str(pkt.seqNo)):
                        #toggling the sequence number if the packet has reached properly
                        gseqNo = int(not (pkt.seqNo))

                        print("gseqNo:"+str(gseqNo))
                        self.acknowledgment=None
                        break
                    
                    if( self.acknowledgment != str(pkt.seqNo)):
                        print("Ack != Seq")
                        break
                                    
                #print("sender: before main and ack join")
                ackthread.join()
                #print("sender:main and ack Threads joined")
   
    #receiver
    def read(self):
        retmsg=""
        expected_seq_num = 0
        last =0
        while last==0:
            
            try:
                data, self.clientAddress = self.ourSocket.recvfrom(MAX_SIZE_BYTES)#UDP recvfrom #######PAUSE HERE
                data = data.decode('ascii')
                last=int(data.split("|")[3])
                
                print("receiver: msg received "+data+str(self.clientAddress))
            except:
                continue
                
            
            if  self.checksum(data,1) != "1111111111111111" : # corrupted packet received relay previous acknowledgement
                #final=str(not expected_seq_num)+ "|ACK"
                print("checksum " + str(self.checksum(data,1)))
                return_msg=str(int(not expected_seq_num))+"|ACK"
                retpkt=packet(return_msg)
                finalPacket = str(retpkt.checksum) + delimiter + str(retpkt.length)+delimiter+ retpkt.msg #pkt.msg is "0|ACK" or "1|ACK"       
                finalPacket=finalPacket.encode('ascii')
                print("receiver:bp1")
                self.ourSocket.sendto(finalPacket, self.clientAddress )                   
        
            elif expected_seq_num != int(data.split("|")[1]):
                return_msg=str(int(not expected_seq_num))+"|ACK"
                retpkt=packet(return_msg)
                finalPacket = str(retpkt.checksum) + delimiter + str(retpkt.length)+delimiter+ retpkt.msg #pkt.msg is "0|ACK" or "1|ACK"       
                finalPacket=finalPacket.encode('ascii')
                print("ExceptedSeqnum :" + str(expected_seq_num)+"Seq number:" + str(int(data.split("|")[1])))
                print("receiver:bp2")
                self.ourSocket.sendto(finalPacket, self.clientAddress )                   

            elif expected_seq_num == int(data.split("|")[1]):
                retmsg+=data.split("|")[4]
                return_msg=str(int(expected_seq_num))+"|ACK"
                retpkt=packet(return_msg)
                finalPacket = str(retpkt.checksum) + delimiter + str(retpkt.length)+delimiter+ retpkt.msg #pkt.msg is "0|ACK" or "1|ACK"       
                finalPacket=finalPacket.encode('ascii')
                print("ExceptedSeqnum :" + str(expected_seq_num)+"Seq number:" + str(int(data.split("|")[1])))
                print("receiver:bp3")
                self.ourSocket.sendto(finalPacket, self.clientAddress)                   
                expected_seq_num = int(not expected_seq_num) #Toggle expected sequence numbers
           
        
        return retmsg , self.clientAddress
                      
        
    #TODO:write a fn for checksum generation
    # checksum functions needed for calculation checksum
    def checksum(self, msg,flag):
        return "1111111111111111"
        s = 0

        # loop taking 2 characters at a time
        for i in range(0, len(msg), 2):
            if(i==len(msg)-1):
                w=ord(msg[i]) + ( 0 << 8)
            else :
                w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
            s = s + w

        s = (s>>16) + (s & 0xffff)
        s = s + (s >> 16)

        if(flag==1):
            return s 

        #complement and mask to 4 byte short
        s = ~s & 0xffff
        print(s)
        return s

  
                 
if __name__ == "__main__":
    #gen=chunkstring("Thisisabigmessage",3)
    #print(type(list(gen)[0]))        
    string=b'abcde'   
    print(string)
    print(type(string.decode("utf-8")))

    checksum()
        
    

