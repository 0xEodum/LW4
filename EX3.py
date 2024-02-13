import ipaddress

def parse_subnet(input_line):
    """Parses a single line of input into a flag (blacklist/whitelist) and subnet."""
    flag = input_line[0]  # '+' for whitelist, '-' for blacklist
    subnet = input_line[1:].strip()  # Remove leading flag and any whitespace
    return flag, subnet

def cidr_to_range(subnet):
    """Converts a CIDR subnet to a range of IP addresses."""
    network = ipaddress.ip_network(subnet, strict=False)
    return int(network.network_address), int(network.broadcast_address)

def ip_int_to_str(ip_int):
    """Converts an integer IP address back to its string representation."""
    return str(ipaddress.ip_address(ip_int))

def range_to_cidr(start_ip, end_ip):
    """Converts a range of IP addresses back to CIDR notation."""
    start_ip_str = ip_int_to_str(start_ip)
    end_ip_str = ip_int_to_str(end_ip)
    return [str(ipaddr) for ipaddr in ipaddress.summarize_address_range(ipaddress.IPv4Address(start_ip_str), ipaddress.IPv4Address(end_ip_str))]

def check_conflict(blacklist, whitelist):
    """Checks for conflicts between blacklisted and whitelisted IP ranges."""
    for b_range in blacklist:
        for w_range in whitelist:
            if b_range[0] <= w_range[1] and w_range[0] <= b_range[1]:
                return True  # Conflict detected
    return False  # No conflict found

def optimize_blacklist(blacklist):
    """Optimizes the blacklist by merging subnets where possible."""
    sorted_blacklist = sorted(blacklist, key=lambda x: x[0])
    optimized = []
    current_start, current_end = sorted_blacklist[0]

    for start, end in sorted_blacklist[1:]:
        if start <= current_end + 1:
            current_end = max(current_end, end)
        else:
            optimized.extend(range_to_cidr(current_start, current_end))
            current_start, current_end = start, end

    optimized.extend(range_to_cidr(current_start, current_end))
    return optimized

# Example data for testing
subnets = [
    "-127.0.0.4/31",
    "+127.0.0.8",
    "+127.0.0.0/30",
    "-195.82.146.208/29",
    "-127.0.0.6/31"
]

blacklist, whitelist = [], []
for input_line in subnets:
    flag, subnet = parse_subnet(input_line)
    start_ip, end_ip = cidr_to_range(subnet)
    if flag == '-':
        blacklist.append((start_ip, end_ip))
    else:
        whitelist.append((start_ip, end_ip))

if check_conflict(blacklist, whitelist):
    print("-1")
else:
    optimized_blacklist = optimize_blacklist(blacklist)
    print(len(optimized_blacklist))
    for subnet in optimized_blacklist:
        print(subnet)
