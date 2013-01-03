#! /usr/bin/env python2.7
from socket import *
import thread
from time import sleep
# config content
host='0.0.0.0'
inport=1234
outport=1235
TTL=20
# end of config content
insock=socket(AF_INET,SOCK_DGRAM)
insock.bind((host,inport))
outsock=socket(AF_INET,SOCK_DGRAM)
outsock.bind((host,outport))
_addrlist={}
pktlen=2048
def forward():
	while 1:
		data,inaddr = insock.recvfrom(pktlen)
		forwardlist(data)
	insock.close()
	outsock.close()

def access():
	while 1:
		data,accaddr = outsock.recvfrom(pktlen)
		addAddrlist(accaddr)

def forwardlist(data):
	for addr in _addrlist.keys():
		outsock.sendto(data,addr)

def addAddrlist(addr):
	if addr not in _addrlist.keys():
		print "add ",addr
	_addrlist[addr]=0

def incTime():
	global _addrlist
	_addrlist={k:v+1 for k,v in _addrlist.iteritems()}

def delTimeOut():
	global _addrlist
	new={k:v for k,v in _addrlist.iteritems() if v <= TTL}
	# stat timeout addrlist
	diff=[k for k in _addrlist.keys() if k not in new.keys()]
	if len(diff)!=0:
		print "timeout: ",diff
	_addrlist=new

def timer():
	while 1:
		sleep(1)
		delTimeOut()
		incTime()

if __name__=="__main__":
	thread.start_new(access,())
	thread.start_new(timer,())
	forward()
