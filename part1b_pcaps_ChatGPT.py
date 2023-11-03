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

def extract_unique_ips(pcap_file):
    unique_src_ips = set()
    unique_dst_ips = set()

    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                unique_src_ips.add(inet_to_str(ip.src))
                unique_dst_ips.add(inet_to_str(ip.dst))

    return sorted(unique_src_ips), sorted(unique_dst_ips)


def print_packet_info(pcap_file):
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        packet_info = []

        packet_number = 0
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                packet_info.append((packet_number, ip.src, ip.dst))
                packet_number += 1

        packet_info.sort(key=lambda x: x[0])  # Sort by packet number

        for packet in packet_info:
            print(f"Packet Number: {packet[0]}, Source IP: {inet_to_str(packet[1])}, Destination IP: {inet_to_str(packet[2])}")


if __name__ == "__main__":
    pcap_file_1 = "ass1_2.pcap"
    pcap_file_2 = "ass1_3.pcap"

    # Task 1: List unique source and destination IPs for both pcap files
    unique_src_ips_1, unique_dst_ips_1 = extract_unique_ips(pcap_file_1)
    unique_src_ips_2, unique_dst_ips_2 = extract_unique_ips(pcap_file_2)

    print("PCAP 1 Unique Source IPs:", unique_src_ips_1)
    print("PCAP 1 Unique Destination IPs:", unique_dst_ips_1)
    print("PCAP 2 Unique Source IPs:", unique_src_ips_2)
    print("PCAP 2 Unique Destination IPs:", unique_dst_ips_2)

    # Task 2: Print packet information for both pcaps
    print("\nPacket Information for PCAP 1:")
    print_packet_info(pcap_file_1)

    print("\nPacket Information for PCAP 2:")
    print_packet_info(pcap_file_2)