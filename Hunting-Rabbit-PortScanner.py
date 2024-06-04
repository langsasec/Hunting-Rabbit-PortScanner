import argparse
import socket
import time

import concurrent.futures
import ipaddress


def check_host_alive(host, port, timeout,verbose=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    if verbose:
        print('[+] Scanning', host, port)
    try:
        sock.connect((host, port))
        sock.close()
        return True
    except Exception as e:
        return False


def scan_port(host, port, timeout, results,verbose=False):
    if check_host_alive(host, port, timeout,verbose):
        results.append(port)


def scan_host(host, port_range, timeout, results, verbose=False):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for port in parse_ports(port_range):
            futures.append(executor.submit(scan_port, host, port, timeout, open_ports,verbose))
        concurrent.futures.wait(futures)
    if open_ports:
        if verbose:
            print(f'{host} is alive')
            print(f'{host} has open ports: {", ".join(map(str, open_ports))}')
        results.append((host, open_ports))
    else:
        if verbose:
            print(f'{host} is not alive')


def scan_network(network, port_range, timeout, max_workers=1000, verbose=False):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for host in ipaddress.IPv4Network(network):
            futures.append(executor.submit(scan_host, str(host), port_range, timeout, results, verbose=verbose))
        concurrent.futures.wait(futures)
    return results


def parse_ports(port_range):
    ports = []
    for item in port_range.split(','):
        if '-' in item:
            start, end = item.split('-')
            start = int(start)
            end = int(end)
            ports.extend(range(start, end+1))
        else:
            ports.append(int(item))
    return ports


parser = argparse.ArgumentParser(description='Hunting-Rabbit-PortScanner       author:浪飒')
parser.add_argument('network', help='Network to scan (e.g. "192.168.0.1" or "192.168.0.0/24")')
parser.add_argument('-p', '--ports', default='21,22,23,25,53,80,81,88,89,110,113,119,123,135,139,143,161,179,199,389,427,443,445,465,513,514,515,543,544,548,554,587,631,646,873,902,990,993,995,1080,1433,1521,1701,1720,1723,1755,1900,2000,2049,2121,2181,2375,2376,3128,3306,3389,3500,3541,3689,4000,4040,4063,4333,4369,4443,4488,4500,4567,4899,5000,5001,5004,5006,5007,5008,5050,5060,5104,5222,5223,5269,5351,5353,5432,5555,5601,5632,5800,5801,5900,5901,5938,5984,5999,6000,6001,6379,6443,6588,6665,6666,6667,6668,6669,7001,7002,7077,7443,7574,8000,8001,8008,8010,8080,8081,8082,8086,8088,8090,8091,8181,8443,8484,8600,8649,8686,8787,8888,9000,9001,9002,9003,9009,9042,9050,9071,9080,9090,9091,9200,9300,9418,9443,9600,9800,9871,9999,10000,11211,12345,15672,16010,16080,16384,27017,27018,50050',
                    help='Ports to scan (e.g. "80" or "1-65535", default: %(default)s)')
parser.add_argument('-t', '--timeout', type=float, default=0.5,
                    help='TCP connection timeout in seconds (default: %(default)s)')
parser.add_argument('-w', '--workers', type=int, default=64,
                    help='Maximum number of worker threads for the scan (default: %(default)s)')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
args = parser.parse_args()

network = args.network
port_range = args.ports
timeout = args.timeout
max_workers = args.workers

start_time = time.time()

print(f'[*] Scanning network {network} ({port_range})...')

results = scan_network(network, port_range, timeout, max_workers=max_workers, verbose=args.verbose)

end_time = time.time()
elapsed_time = end_time - start_time

if results:
    print(f'[+] Found open ports on {len(results)} host(s):')

    with open(f'{network.replace("/","_")}.txt', 'w') as f:
        for host,port in results:
            for port in port:
                f.write(f'{host}:{port}\n')
                print(f'{host}:{port}')

    print(f'[+] Open ports saved to {network.replace("/","_")}.txt')
else:
    print('[-] No open ports found on any host.')

print(f'[+] Scan completed in {elapsed_time:.2f} seconds.')
