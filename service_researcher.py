from other_function.directory_searcher import http_directory_researcher

def service_searcher(remote_service, remote_port, remote_ip):
    for service_name in remote_service:
        if service_name == 'http':
            http_directory_researcher(remote_port[remote_service.index(service_name)], remote_ip)
    print("end")