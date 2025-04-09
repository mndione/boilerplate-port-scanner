import socket
import re
from common_ports import  ports_and_services

def get_open_ports(target, port_range, verbose = False):
    open_ports = []
    
    for port in range(port_range[0], port_range[1] + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(5)
            sock.connect((target, port))
            
            open_ports.append(port)
            
        except  socket.gaierror:
            sock.close()
            #print(re.findall(r"^\d+\.\d+\.\d+\.\d+$", target))
            if len(re.findall("^\\d+\\.\\d+\\.\\d+\\.\\d+$", target)) == 1:
                return "Error: Invalid IP address"
            else:
                return "Error: Invalid hostname"

        except ConnectionRefusedError:
            pass
            
        except socket.timeout:
            pass
        
        except OSError:
            pass
        
        sock.close()
            
    if verbose:
        addrinfo = socket.getaddrinfo(target, None, socket.AF_INET, socket.SOCK_STREAM, 0, socket.AI_CANONNAME)
        _, _, _, url, ip = addrinfo[0]
        ip, _ = ip

        if url == ip:
            try:
                host, _, _ = socket.gethostbyaddr(ip)
                url = socket.getfqdn(host)
            except socket.herror:
                url = ip
        
        str_open_ports = f'Open ports for {url}'
        if ip != url:
            str_open_ports += f' ({ip})'
        
        str_open_ports += f'\n{"PORT":<9}SERVICE\n'

        for port in open_ports:
            str_open_ports += f'{port:<9}{ports_and_services[port]}\n'
        open_ports = str_open_ports.strip('\n')
    
    return(open_ports)