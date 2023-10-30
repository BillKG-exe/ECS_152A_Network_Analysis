import dpkt

def parse_pcap(pcap_file):
    protocols_count = {"http": 0, "https": 0, "icmp": 0, "ftp": 0, "ssh": 0}

    # read the pcap file
    f = open(pcap_file, 'rb')
    pcap = dpkt.pcap.Reader(f)

    # iterate over packets
    for timestamp, data in pcap:

        # convert to link layer object
        eth = dpkt.ethernet.Ethernet(data)

        # do not proceed if there is no network layer data
        if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
            continue
        
        # extract network layer data
        ip = eth.data

        if isinstance(ip.data, dpkt.icmp.ICMP) or isinstance(ip.data, dpkt.icmp6.ICMP6):
            protocols_count['icmp'] += 1
            continue

        # do not proceed if there is no transport layer data
        if not isinstance(ip.data, dpkt.tcp.TCP):
            continue

        # extract transport layer data
        tcp = ip.data

        # do not proceed if there is no application layer data
        # here we check length because we don't know protocol yet
        if not len(tcp.data) > 0:
            continue

        # extract application layer data
        ## if destination port is 80, it is a http request
        if tcp.dport == 80 or tcp.sport == 80:
            protocols_count["http"] += 1
        elif tcp.dport == 443 or tcp.sport == 443:
            protocols_count["https"] += 1   
        elif tcp.dport == 20 or tcp.sport == 20 or tcp.dport == 21 or tcp.sport == 21:
            protocols_count["ftp"] += 1
        elif tcp.dport == 22 or tcp.sport == 22:
            protocols_count["ssh"] += 1
    

    f.close()
    print(protocols_count)

def main():
    pcaps = ["example.pcap", "ftp.pcap", "httpforever.pcap", "ping.pcap", "ssh.pcap"]
    
    for pcap_file in pcaps:
        print(f"{pcap_file} report: ")
        parse_pcap(pcap_file)
        print()

    return

main()