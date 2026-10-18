#!/usr/bin/env python3

#Liam Patten

from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket, timeout
import re
import sys
import time

#constants:
PING_COUNT=10
TIMEOUT_SECONDS=1.0
MAX_DATAGRAM_BYTES = 1024
SERVER_HOST = "128.180.120.92"
SERVER_PORT = 4041

def main():

    #prints ip and port of server, along with number of pings and the duration of timeout
    print(f'\nTarget: {SERVER_HOST}:{SERVER_PORT}/udp')
    print(f'Pings: {PING_COUNT}; timeout: {TIMEOUT_SECONDS} second')

    #creates the socket with dgram for udp connection and af_inet for ipv4
    clientSocket = socket(AF_INET,SOCK_DGRAM)
    #sets the timeout duration for the socket.
    clientSocket.settimeout(TIMEOUT_SECONDS)
    # clientSocket.connect((SERVER_HOST,SERVER_PORT))

    #loop to ping server 10 times
    for i in range(1,11):
        try:
            #message variable to show 
            msg='Ping '+str(i)+' '+str(time.time())
            
            #utf 8 encoded message
            encoded = msg.encode('utf-8')

            #variable to store time before socket sends message
            begin = time.perf_counter()

            #socket sends encoded message to server
            clientSocket.sendto(encoded,(SERVER_HOST,SERVER_PORT))
            #variable to store response from the server
            response = clientSocket.recvfrom(MAX_DATAGRAM_BYTES)

            #variable to show end of sending and recieving 
            end = time.perf_counter()

            #variable to get decoded message from server
            decoded = response[0].decode('utf-8',errors='replace')

            #check encoded message sent equals one recieved
            if msg.upper() == decoded:
                #shows reply from server. prints the decoded message and the sequence number
                #also prints the RTT for the message
                print(f'Reply from {SERVER_HOST}:{SERVER_PORT}: {decoded} | sequence = {i} | RTT = {end-begin} s')
            else:
                print(f'message recieved does not equal one sent')
        
        #timeout handler. prints that the request timeout,what duration the timeout is and sequence number
        except (timeout):
            print(f'Request timed out | sequence = {i} | timeout = {TIMEOUT_SECONDS} s')
        except (OSError, RuntimeError) as error:
            print(f"ERROR: {error}")
            return 1
    clientSocket.close()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())