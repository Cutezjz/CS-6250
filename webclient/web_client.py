'''
/==============================
 Author: Shiqi Zheng
 Date created: 04/06/2016
 Summary: Create a web-client
==============================/ 
''' 

import socket
import sys
from urlparse import urlparse

#Header Parser
def parse(s):
	s=s.split("\r\n")
	header={}
	for i in range(1,len(s)):
		m=s[i].split(": ")
		if(len(m)>1):
			key,value = m[0],m[1]
		header[key]=value
	return header

def main():
	#Initialization
	header ={}
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	addr = urlparse(sys.argv[1])
	host =socket.gethostbyname(addr.hostname)
	message = "GET "+ sys.argv[1]+" HTTP/1.1\r\nHost:"+host+"\r\nConnection: close\r\n\r\n" 

	# establish connection
	try:
		sock.connect((host,80))
	except socket.gaierror, err:
		print "cannot resolve hostname: ", name, err
	
	# send message and receive response. 
	try :
		sock.sendall(message)

		print ("Send Messsage Header: \n" + message)

		response = sock.recv(4096)

	except socket.error:
		print 'Send failed'
		sys.exit()
	
	#parse header
	listRes=response.split("\r\n\r\n")
	head= listRes[0]
	print ("Receive Message Header: \n" + head + "\n")
	
	#save data if header includes 200 OK and Content_length
	if("200 OK" in head):
		if("Content-Length" in head):
			f=open(sys.argv[2],"w")
			size=0
			for i in range(1,len(listRes)):
				size+=len(listRes[i])
				if(i>1): 
					size+=4
					f.write("\r\n\r\n")
				f.write(listRes[i])
			

			header = parse(head)
		
			amount_received = size
			amount_expected = int(header["Content-Length"])
			
			while amount_received < amount_expected:
				data = sock.recv(4096)
				amount_received += len(data)
				f.write(data)
			f.close()
		
	sock.close()
if __name__=="__main__":
	main()