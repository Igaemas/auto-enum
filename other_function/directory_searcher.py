import requests
import sys
from configparser import ConfigParser
parser = ConfigParser()
parser.read('config.ini')

class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

try:
    if sys.argv[2]:
        output_file_name = sys.argv[2]
except:
    try:
        output_file_name = parser.get('basic_config', 'file_name')
    except:
        output_file_name = "tryout.txt"

wordlist_file_var = parser.get('wordlists', 'directory')
wordlist_txt_file = open(wordlist_file_var).read()
wordlist = wordlist_txt_file.splitlines()

valid_directory_list = []

def http_directory_researcher(remote_port, remote_ip):
    
    output_file = open(output_file_name, 'a')
    
    print(f"\ndirectory enumeration on port {remote_port} with this wordlist : {wordlist_file_var}.\n")
    output_file.write(f"\ndirectory enumeration on port {remote_port} with this wordlist : {wordlist_file_var}.\n")
    
    for directory in wordlist:
        url_request = f"http://{remote_ip}:{remote_port}/{directory}/"
        
        r = requests.get(url_request)
        if r.status_code == 404:
            pass
        else:
            valid_directory_list.append(directory)
    
    print("valid directory : ")
    output_file.write("\nvalid directory : ")
    for valid_directory in valid_directory_list:
        print(colors.GREEN + "   " + valid_directory + colors.RESET)
        output_file.write("\n   " + valid_directory)
    output_file.write('\n')
        
    output_file.close()