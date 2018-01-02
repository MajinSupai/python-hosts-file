#A module for easily and programmatically modifying a hosts file
#
#@author MajinSupai

import HostTools

class HostsFile(object):
	def __init__(self, filepath):
		self.filepath = filepath
		
		with open(filepath, 'r') as textFile:
			text = textFile.read()
		
		self.lines = _parseHosts(text)
	
	def __str__(self):
		output = ''
		
		for notComment, comment, ip, hosts in self.lines:
			if notComment is None: #Line is empty
				output += '\n'
				continue
				
			if notComment: #Line is a normal line
				outputLine = ip + TAB_CHAR + TAB_CHAR.join(hosts)
				
				if comment:
					outputLine += TAB_CHAR + '#' + comment
				
			else: #Line is a comment
				outputLine = '#' + comment
			
			output += outputLine + '\n'
		
		
		return output[: -1] #It will have an unnecessary newline
	
	def __iter__(self):
		for line in self.lines:
			if line[0]:
				yield (line[2], line[3]) #Yielding ip and hosts
	
	def __in__(self, search):
		return self.test(search) #Tests if search is an existing ip or host
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		self._update()
	
	
	def _iterAll(self):
		for line in self.lines:
			if line[0] is None: #Line is empty
				yield (False, None, None)
			
			else:
				yield (line[0], line[2], line[3]) #Yielding notComment, ip, and hosts
		
	def _addEntry(self, ip, hosts, comment):
		self.lines.append([True, comment, ip, hosts])
	
	def _addAlias(self, index, alias, comment=None):
		line = self.lines[index]
		
		if comment:
			line[1] += ';' + TAB_CHAR + comment
			
		line[3].append(alias)
	
	def _removeEntry(self, index):
		del self.lines[index]
	
	def _setIndex(self, index, ip, hosts, comment):
		self.lines[index] = [True, comment, ip, hosts]
	
	def _update(self):
		text = str(self)
		
		with open(self.filepath, 'w') as textFile:
			textFile.write(text)
		
		
	def getIndex(self, search):
		search = search.lower()
		
		for index, (notComment, ip, hosts) in enumerate(self._iterAll()):
			if notComment:
				if (ip == search) or (search in hosts):
					return index
		
		return None
	
	def getIndexByIP(self, searchIP):
		for index, (notComment, ip, hosts) in enumerate(self._iterAll()):
			if notComment & (ip == searchIP):
				return index
		
		return None
	
	def getIndexByHost(self, searchHost):
		searchHost = searchHost.lower() #Hosts are case-insensitive
		
		for index, (notComment, ip, hosts) in enumerate(self._iterAll()):
			if notComment:
				if searchHost in hosts:
					return index
		
		return None
	
	def find(self, search):
		search = search.lower()
		
		for ip, hosts in self:
			if ip == search:
				return host
			
			elif search in hosts:
				return ip
		
		return None
		
	def findHost(self, searchHost):
		searchHost = searchHost.lower()
		
		for ip, hosts in self:
			if searchHost in hosts:
				return ip
		
		return None
	
	def findIP(self, searchIP):
		"""Returns host for IP. None if not found"""
		
		for ip, hosts in self:
			if ip == searchIP:
				return hosts
		
		return None
	
	def test(self, search):
		"""Tests if search is a host or ip that exists in file"""
		
		return bool(self.find(search))
	
	def testHost(self, searchHost):
		"""Tests if host exists in file"""
		
		return bool(self.findHost(searchHost))
	
	def testIP(self, searchIP):
		"""Tests if ip exists in file"""
		
		return bool(self.findIP(searchIP))
	
	def remove(self, removal):
		"""Removes an IP or host"""
		
		indexIP  = self.getIndexByIP(removal)
		indexHost = self.getIndexByHost(removal)
		
		print(indexIP, indexHost)
		
		if indexIP is not None:
			self._removeEntry(indexIP)
		
		elif indexHost is not None:
			hostLine = self.lines[indexHost]
			
			currentHosts = hostLine[3]
			
			if len(currentHosts) > 1: #Only remove single host
				currentHosts.remove(removal)
			   
			else: #Remove entire line
				self._removeEntry(indexHost)
	
	def setHost(self, ip, host, comment=None):
		"""Either updates a host/ip or adds an entry"""

		host = host.lower()
		
		if not HostTools.verifyIP(ip):
			raise ValueError('ip incorrectly formatted')
		
		if not HostTools.verifyHost(host):
			raise ValueError('host incorrectly formatted')
			
		indexIP = self.getIndexByIP(ip)
		indexHost = self.getIndexByHost(host)
		
		if indexIP == indexHost:
			if indexIP is None: #Entry must not exist
				self._addEntry(ip, [host], comment)
			
			else: #Exact entry already exists. Do nothing.
					pass
		
		elif indexIP is None: #Host must already exist, but not IP. Overwriting it.
			hostLine = self.lines[indexHost]

			currentHosts = hostLine[3]

			if len(currentHosts) > 1: #Move aliases to another line
				currentHosts.remove(host) #Remove host which is going to be reassigned
				
				self._addEntry(ip, [host], comment)
			   
			else:
				self._setIndex(indexHost, ip, [host], comment)
			
		elif indexHost is None: #IP must already exist, but not host. Adding alias.
			self._addAlias(indexIP, host, comment)
			
		else: #Both IP and host exist and are separate entries. Cannot overwrite both.
			raise Exception('multiple matching references found. Remove one/both and try again')

			
def _parseHosts(text):
	text = text.strip('\n')
	
	if not text: #File is empty
		return []
	
	lines = []
	
	for index, line in enumerate(text.split('\n')):
		line = line.strip()
		
		if not line: #Line is empty
			lines.append([None, None, None, None])
			continue
		
		if line.startswith('#'): #Line is only a comment
			notComment = False
			comment = line[1:]
			ip = None
			hosts = None
			aliases = None
			
		else: #Line is a normal line
			notComment = True
			
			try:
				commentStart = line.index('#')
			
			except ValueError:
				commentStart = -1
			
			if commentStart != -1: #The line contains a comment, so separate it
				comment = line[commentStart + 1:]
				line = line[: commentStart]
			
			else:
				comment = None
			
			#Change tabs into spaces for easier splitting
			#Blank entries will be removed, so duplicates in a row aren't an issue
			line = line.replace('\t', ' ')
			
			splitLine = line.split(' ')
			
			line = []
			
			#Remove all empty strings
			for val in splitLine:
				if val: #Since it split with single spaces, there will be empty strings
					line.append(val)
			
			
			if len(line) >= 2:
				ip = line[0]
				hosts = [x.lower() for x in line[1:]] #Hosts are case-insensitive
				
				if not HostTools.verifyIP(ip):
					raise Exception('hosts file is malformed on line {} (Improper IP)'.format(index))
				
				for host in hosts:
					if not HostTools.verifyHost(host):
						raise Exception('hosts file is malformed on line {} (Improper host)'.format(index))
			
			else:
				raise Exception('hosts file is malformed on line {} (Improper formatting)'.format(index))
	
		lines.append([notComment, comment, ip, hosts])
	
	return lines

TAB_CHAR = '	'
