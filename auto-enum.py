# importation du module nmap
import nmapthon as nm

import sys

from configparser import ConfigParser

#
# CLASS
#
class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    
class errors:
    config_file = 'Can\'t find this parameter in the \"config.ini\" file :\n   '
    argv = 'No arguments in the command for:\n   '
    running_script = 'Can\'t run : '

#
# Variable 
#
parser = ConfigParser()
parser.read('config.ini')

remote_ip_address = sys.argv[1]
remote_open_ports = []

try:
    all_ports_number = parser.get('speed_nmap', 'ports')
except:
    print(errors.config_file + colors.RED + 'speed_nmap : ports' + colors.RESET)

try:
    speed_nmap_arg = parser.get('speed_nmap', 'arg')
except:
    print(errors.config_file + colors.RED + 'speed_nmap : arg' + colors.RESET)

try:    
    complete_nmap_arg = parser.get('complete_nmap', 'arg')
except:
    print(errors.config_file + colors.RED + 'complete_nmap : arg' + colors.RESET)

try:
    if sys.argv[2]:
        output_file_name = sys.argv[2]
except:
    print(errors.argv + colors.RED + 'output_file_name' + colors.RESET)
    try:
        output_file_name = parser.get('basic_config', 'file_name')
    except:
        print(errors.config_file + colors.RED + 'basic_config : file_name' + colors.RESET)
        output_file_name = "tryout.txt"

print("\nOutput file is : " + colors.GREEN + output_file_name + colors.RESET + "\n")
    
# 
# fonction to do a speed enumeration of port with nmap
#
def speed_nmap(remote_ip_address, ports_range, nmap_arg):
    print("\n--------------------------------\n--- starting speed port scan ---\n--------------------------------\n")
    
    port_scan = nm.NmapScanner(
        remote_ip_address, 
        arguments=nmap_arg, 
        ports=ports_range
    )
    
    port_scan.run() 
    output_file = open(output_file_name, "a")
        
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
                print(colors.GREEN + "    " + str(port) + colors.RESET)
                remote_open_ports.append(str(port))
                output_file.write("    " + str(port) + "\n")     

    output_file.close()
    
def complete_nmap(remote_ip_address, ports_range, nmap_arg):
    print("\n-----------------------------------\n--- starting complete port scan ---\n-----------------------------------")
    
    scanner = nm.NmapScanner(
        remote_ip_address, 
        arguments=nmap_arg, 
        ports=ports_range
    )
    
    scanner.run()
    output_file = open(output_file_name, "a")
    
    print("\nOS information :")
    output_file.write("\nOS information :")
    
    for os_match, acc in scanner.os_matches(remote_ip_address):
        print('   OS Match: {}\tAccuracy:{}%'.format(os_match, acc))
        output_file.write('   OS Match: {}\tAccuracy:{}%\n'.format(os_match, acc))
    
    fingerprint = scanner.os_fingerprint(remote_ip_address)
    if fingerprint is not None:
        print('   Fingerprint: {}'.format(fingerprint))
        output_file.write('   Fingerprint: {}\n'.format(fingerprint))

    for most_acc_os in scanner.most_accurate_os(remote_ip_address):
        print('   Most accurate OS: ' + colors.GREEN + f'{most_acc_os}' + colors.RESET)
        output_file.write('   Most accurate OS: ' + f'{most_acc_os}\n')
    
    # for every host scanned
    for host in scanner.scanned_hosts():
        # for every protocol scanned for each host
        for proto in scanner.all_protocols(host):
            # for each scanned port
            for port in scanner.scanned_ports(host, proto):
                # Get service object
                service = scanner.service(host, proto, port)
                print(f"\nport : {port}")
                output_file.write(f"\nport : {port}")
                if service is not None:
                    print(colors.GREEN + f"   {service.name} | {service.product}" + colors.RESET)
                    output_file.write(f"   {service.name} | {service.product}\n")
                    for cpe in service.all_cpes():
                        print(f"   CPE: {cpe}")
                        output_file.write(f"   CPE: {cpe}\n")
                    for name, output in service.all_scripts():
                        print(f"   Script: {name}\n     Output: {output}")
                        output_file.write(f"   Script: {name}\n     Output: {output}\n")
                    # You could also do print(str(service))
                    # You could also know if 'ssh-keys' script was launched and print the output
                    if 'ssh-keys' in service:
                        print("{}".format(service['ssh-keys']))
                        output_file.write("{}\n".format(service['ssh-keys']))
                        
    output_file.close()

#
# running fonction
#
try:
    speed_nmap(remote_ip_address, all_ports_number, speed_nmap_arg)
except:
    print(errors.running_script + colors.RED + 'speed_nmap' + colors.RESET)
    exit()

try:
    complete_nmap(remote_ip_address, remote_open_ports, complete_nmap_arg)
except:
    print(errors.running_script + colors.RED + 'complete_nmap' + colors.RESET)
    exit()