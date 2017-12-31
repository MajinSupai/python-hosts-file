import Hosts
import HostTools

#Example for setting a host for an IP on the current subnet

IPs = ['192.168.1.200', '10.0.0.61']
HOSTS_LOCATION = 'C:\\Users\\wesle\\Documents\\Test.txt'

localIP = HostTools.getLocalIP()

connectIP = None

for IP in IPs:
    if HostTools.testSubnet(localIP, IP):
        connectIP = IP
        break

if not connectIP:
    print('could not find matching IP')

else:
    with Hosts.HostsFile(HOSTS_LOCATION) as hosts:
        hosts.setHost(connectIP, 'pc-loc', 'pointing toward pc on different subnets')
