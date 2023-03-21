from configparser import ConfigParser
parser = ConfigParser()
parser.read('config.ini')

wordlist = parser.get('wordlists', 'directory')

def http_directory_researcher(remote_port, remote_ip):
    print("test", remote_port, remote_ip)