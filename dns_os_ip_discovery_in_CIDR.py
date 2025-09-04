import os,ipaddress,signal,sys,subprocess,socket,re,platform


def sig_handler(sig, frame):
    print("\n\nExiting program...\n")
    sys.exit(1)


signal.signal(signal.SIGINT, sig_handler)

def ping_host(ip_address):
    """
    Pings the host to check if it is reachable.
    Returns True if reachable, False otherwise.
    """
    os_name = platform.system().lower()
    if os_name == "windows":
        command = ["ping", "-n", "1", "-w", "1000", ip_address]  # 1s
    elif os_name == "darwin":  # macOS
        command = ["ping", "-c", "1", "-W", "1000", ip_address]  # ms en macOS
    else:  # linux
        command = ["ping", "-c", "1", "-W", "1", ip_address]     # 1s por respuesta
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

    if result.returncode == 0:
        output = result.stdout
        # Search TTL value in ping's output
        ttl_match = re.search(r'(?:ttl|TTL)\s*[=:]\s*(\d+)', output)
        if ttl_match:
            ttl_value = ttl_match.group(1)
            if "12" in ttl_value:
                return ip_address,"Windows"
            else:
                return ip_address,"Linux"



def get_machine_name(ip_address):
    """
    Returns the machine name for a given IP address.
    If the hostname cannot be resolved, returns 'Unknown'.
    """
    try:
        return socket.gethostbyaddr(ip_address)[0]
    except socket.herror:
        return 'Unknown'

if __name__ == "__main__":
    cidr=input("Enter CIDR to search from:\t")
    ip_range=cidr.split("/")[0].replace(".","_")
    with open(f"{ip_range}.txt","w") as f:
        for ip in ipaddress.IPv4Network(f"{cidr}"):
            resultado=ping_host(str(ip))
            if resultado != None:
                ip4=str(resultado[0])
                so=resultado[1]
                machine_name = get_machine_name(ip4)
                print(f"{machine_name},{ip4},{so}")
                f.write(f"{machine_name},{ip},{so}\n")
            

                

