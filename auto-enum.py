# importation du module nmap
import nmapthon as nm

import sys
from configparser import ConfigParser
parser = ConfigParser()
parser.read('config.ini')

remote_ip_address = sys.argv[1]
all_ports_number = parser.get('speed_nmap', 'ports')
speed_nmap_arg = parser.get('speed_nmap', 'arg')
remote_open_ports = []

# 
# fonction to do a speed enumeration of port with nmap
#
def speed_nmap(remote_ip_address, ports_range, nmap_arg):
    print("\n--- starting speed port scan ---\n")
    
    port_scan = nm.NmapScanner(
        remote_ip_address, 
        arguments=nmap_arg, 
        ports=ports_range
    )
    port_scan.run()
    output_file = open("output.txt", "a")
        
    for host in port_scan.scanned_hosts():
        # Get state, reason and hostnames
        print(f"\n{host} is {port_scan.state(host)}\n")
        output_file.write(f"{host} is {port_scan.state(host)}\n")
        
        # Get scanned protocols
        for proto in port_scan.all_protocols(host):
            # Get scanned ports
            print("open ports :")
            output_file.write("open port :\n")
            for port in port_scan.scanned_ports(host, proto):
                state, reason = port_scan.port_state(host, proto, port)
                print("    " + str(port))
                remote_open_ports.append(str(port))
                output_file.write("    " + str(port) + "\n")     

    output_file.close()
speed_nmap(remote_ip_address, all_ports_number, speed_nmap_arg)