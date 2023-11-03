import dpkt
import socket

def inet_to_str(inet):
    """Convert inet object to a string

        Args:
            inet (inet struct): inet network address
        Returns:
            str: Printable/readable IP address
    """
    #ipv4 
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except:
        pass
    

def unique_ip(fileName):
    pairs = set()

    f = open(fileName, 'rb')
    pcap = dpkt.pcap.Reader(f)

    for timestamp, data in pcap:
        #convert to link layer object
        eth = dpkt.ethernet.Ethernet(data)

        if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
            continue

        ip = eth.data

        if not isinstance(ip.data, dpkt.icmp.ICMP):
            continue

        icmp = ip.data

        pairs.add((inet_to_str(ip.src), inet_to_str(ip.dst)))



    print("Listing the unique source and destination IP addresses from the " + fileName + " file...")
    for pair in pairs:
        src, dst= pair
        print("SOURCE: " + src + " DESTINATION: " + dst)
    print()


def print_packets(fileName):

    count = 1
    f = open(fileName, 'rb')
    pcap = dpkt.pcap.Reader(f)
    print("printing the packet number, source ip address and destination ip address for each packet from the " + fileName + " file...")
    for timestamp, data in pcap:
        #convert to link layer object
        eth = dpkt.ethernet.Ethernet(data)

        if not isinstance(eth.data, dpkt.ip.IP) and not isinstance(eth.data, dpkt.ip6.IP6):
            continue

        ip = eth.data

        if not isinstance(ip.data, dpkt.icmp.ICMP):
            continue

        icmp = ip.data

        print("PACKET NUMBER: " + str(count) + " SOURCE: " + inet_to_str(ip.src) + " DESTINATION: " + inet_to_str(ip.dst) + " TYPE: " + str(icmp.type) + " CODE: " + str(icmp.code))
        count += 1
    print()

   
def main():

    unique_ip('ass1_2.pcap')
    unique_ip('ass1_3.pcap')
    print_packets('ass1_2.pcap')
    print_packets('ass1_3.pcap')

    return
main()
    


