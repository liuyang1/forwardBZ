#! /usr/bin/env python
from socket import *
import thread
from time import sleep
# config content
forward_addr=('0.0.0.0',1235)#public network IP addr
lo_addr=('127.0.0.1',1234)
# end of config
sock=socket(AF_INET,SOCK_DGRAM)
lo=socket(AF_INET,SOCK_DGRAM)
pktlen=2048

def forward():
	while 1:
		data,addr = sock.recvfrom(pktlen)
		lo.sendto(data,lo_addr)
	sock.close()
	lo.close()

def beat():
	while 1:
		sock.sendto("access",forward_addr)
		sleep(10)

if __name__=="__main__":
	if forward_addr[0]=='0.0.0.0':
		print "usage:\n\tmust config public network IP addr"
		exit()
	thread.start_new(beat,())
	forward()
