# Python Hosts File
Module for simplifying programmatic modifications of a hosts file
Obviously, scripts using this must be run in adminstrator/SU mode

# Hosts.py
The Hosts.py file adds the main class used, the HostsFile class.
This class is used to open, modify, and save the hosts file. It must be passed the location of the hosts file

```
hosts = HostsFile(HOSTS_LOCATION)
```

It also has a with notation, which is recommended as it automatically saves changes,

```
with HostsFile(HOSTS_LOCATION) as hosts:
  pass
```

The HostsFile object supports a few methods

```
getIndex        - Returns the line no. of a host or ip
getIndexByIP    - Returns the line no. of an IP
getIndexByHost  - Returns the line no. of a host
find            - Finds a host or ip, then returns the other
findHost        - Finds a host, then returns the IP
findIP          - finds an IP, then returns the hosts
test            - Tests if a host or ip exists
testHost        - Tests if a host exists
testIP          - Tests if an IP exists
remove          - Removes an IP or host
setHost         - Sets an IP, host combination with an optional comment
```

The most-useful of these is the setHost method. The setHost method will set an IP, host combination. Except, it has four different methods of doing this.

```
IP and host are already bound                       - Does nothing
IP is bound to another host                         - Adds host as an alias
Host is bound to another ip                         - Overwrites IP
IP and host are already set, but not to each other  - Raises an exception (Of type Exception)
```

# HostTools.py
HostTools contains a few useful functions, a few of which are used by Hosts.py. It contains

```
verifyHost   - Verifies a hostname is valid
verifyIP     - Verifies an IP is valid
ipToBinary   - Converts an IP to its binary form
getPublicIP  - Gets current public IP
getLocalIP   - Gets current local IP
getIP        - Gets the IP from a hostname (socket.gethostname except returns None instead of raising exception)
```
# Examples
Useful examples can be found within the example python files
