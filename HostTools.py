#Some tools for hosts and IP addresses
#Some functions used by Hosts.py

from urllib import request
import socket, re


DEFAULT_MASK = "255.255.255.0"


def verifyHost(host):
	"""Verifies a hostname is valid"""
	
	#For full documentation on host-name restrictions:
	#https://en.wikipedia.org/wiki/Hostname#Restrictions_on_valid_hostnames
	
	host = host.lower() #Hosts are case-insensitive
	host = host.strip('.') #Remove trailing dot
	
	#Host name must be less than 253 ASCII characters
	if len(host) > 253:
		return False
	
	
	return bool(HOSTNAME_RE.fullmatch(host))			
		
def verifyIP(ip):
	"""Verifies an IP is valid"""
	
	try:
		#Split ip and integer-ize it
		octets = [int(x) for x in ip.split('.')]
	
	except ValueError:
		return False
	
	#First verify length
	if len(octets) != 4:
		return False
	
	#Then check octet values
	for octet in octets:
		if octet < 0 or octet > 255:
			return False
	
	return True

def ipToBinary(ip):
	"""Returns an IP in its binary form"""
	
	if not verifyIP(ip):
		raise ValueError('ip not properly formatted')
	
	#This is performed twice, whoops
	octets = [int(x) for x in ip.split('.')]
	
	#Reverse octets because they're going to be treated like a base-256 number
	octets.reverse()
	
	outputValue = 0
	
	for octet in octets:
		#Shift value then OR the new octet in the "new space"
		outputValue <<= 8
		outputValue |= octet
	
	return outputValue

def getPublicIP():
	"""Returns current public IP"""
	
	return request.urlopen('http://ip.42.pl/raw').read().decode()

def getLocalIP():
	"""Returns current local IP"""
	
	return socket.gethostbyname(socket.gethostname()) #Just a slight hack

def getIP(host):
	"""Returns IP of host"""
	
	try:
		return socket.gethostbyname(host)
	
	except socket.gaierror:
		return None

def testSubnet(ip1, ip2, mask=DEFAULT_MASK):
	"""Tests if two IPs are on the same subnet"""
	
	ip1 = ipToBinary(ip1)
	ip2 = ipToBinary(ip2)
	mask = ipToBinary(mask)
	
	if (ip1 & mask) == (ip2 & mask):
		return True
	
	return False
	


#Regular expression for a valid hostname
HOSTNAME_RE = re.compile('([a-z0-9][a-z0-9-]{,62}\\.)*[a-z0-9][a-z0-9-]{,62}')