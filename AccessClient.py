#! /usr/bin/env python
from socket import *
import thread
from time import sleep
from sys import argv
import getopt

sock=socket(AF_INET,SOCK_DGRAM)
lo=socket(AF_INET,SOCK_DGRAM)
pktlen=2048

def forward(lo_addr):
	while 1:
		data,addr = sock.recvfrom(pktlen)
		lo.sendto(data,lo_addr)
	sock.close()
	lo.close()

def beat(forward_addr):
	while 1:
		sock.sendto("access",forward_addr)
		sleep(10)

def usage():
	print "usage:"
	print "\t%s RemoteIP RemotePort LocalPort"%(argv[0])
	exit()

def main():
	if len(argv)!=4:
		usage()
	remote=(argv[1],int(argv[2]))
	local=('127.0.0.1',int(argv[3]))
	thread.start_new(beat,(remote,))
	forward(local)

if __name__=="__main__":
	main()
