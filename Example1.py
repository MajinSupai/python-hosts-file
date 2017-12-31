import Hosts, HostTools

#In this example, it creates a host titled 'home-pc' which points toward some
#device at home. When you are home, it sets it to the device's local IP. When
#you are away, it sets it to your public IP address. Obviously only useful
#when port forwarding.

HOME_IP = 'HOME_IP_HERE'
LOCAL_IP = 'HOME_LOCAL_IP_HERE'
HOSTS_LOCATION = 'HOSTS_FILE_LOCATION_HERE'


publicIP = HostTools.getPublicIP()

if publicIP == HOME_IP:
    connectIP = LOCAL_IP

else:
    connectIP = HOME_IP

with Hosts.HostsFile(HOSTS_LOCATION) as hosts:
    hosts.setHost(connectIP, 'home-pc', 'Host which always points home')
