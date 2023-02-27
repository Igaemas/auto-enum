# importation du module nmap
import nmapthon as nm

import sys

remote_ip_address = sys.argv[1]
remote_open_ports = []

print("\n--- starting speed port scan ---\n")

port_scan = nm.NmapScanner(remote_ip_address, arguments='-sS -Pn')
port_scan.run()
    
for host in port_scan.scanned_hosts():
    # Get state, reason and hostnames
    print(f"\n{host} is {port_scan.state(host)}\n")
    # Get scanned protocols
    for proto in port_scan.all_protocols(host):
        # Get scanned ports
        print("open ports :")
        for port in port_scan.scanned_ports(host, proto):
            state, reason = port_scan.port_state(host, proto, port)
            print("    " + str(port))
