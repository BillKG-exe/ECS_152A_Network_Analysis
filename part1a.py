import dpkt
import socket

def pcap_report(pcap_file, host):
    protocols_count = {"http": 0, "https": 0, "icmp": 0, "ftp": 0, "ssh": 0}
    destination = None
    ip_timestamps = []

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

        # Extract destination IP
        if isinstance(ip, dpkt.ip.IP):
            dst_ip = socket.inet_ntoa(ip.dst)
            
            # Whenever the destination Ip is equal to that of the first
            # append its timestamp into an array
            if dst_ip.startswith(host):
                ip_timestamps.append(timestamp)

                if destination is None:
                    destination = dst_ip

        if isinstance(ip.data, dpkt.icmp.ICMP) or isinstance(ip.data, dpkt.icmp6.ICMP6):
            protocols_count['icmp'] += 1

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
    print("Application Layer Protocols: ")
    print(protocols_count)
    
    print()

    print(f"Destination IP Address: {destination}")
    print(f"Timestamps: ")
    print(ip_timestamps)

    print("\n")

def main():
    pcaps = {"ping.pcap": "142.250.191.", "example.pcap": '93.184.216', "httpforever.pcap": "146.190.62", "ftp.pcap": "209.51.188.", "ssh.pcap": "205.166.94"}
    
    for key, value in pcaps.items():
        print(f"{key.upper()} Report: ")
        pcap_report(key, value)
        print()

    return

main()