#! /usr/bin/env python
# read from interactive input,and send to remote UDP addr
from socket import *
host = 'localhost'
port = 1234
addr=(host,port)
sock = socket(AF_INET,SOCK_DGRAM)
while 1:
	str=raw_input(">>")
	sock.sendto(str,addr)
sock.close()
