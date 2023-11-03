import socket
import random


# specify server host and port to connect to
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5500


def generatePackets():
    packets = []

    while len(packets) != 1024 * 100:
        packets.append(chr(ord('a')+random.randrange(0, 27)))

    return packets

# open a new datagram socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:

    # Get the list of packets to be sent to server
    packets = generatePackets()

    # Sends 100 packets to the server 
    for packet in packets:
        client_socket.sendto(packet.encode(), (SERVER_HOST, SERVER_PORT))
    
    # Get throughput from server
    reply, _ = client_socket.recvfrom(1024)

    print(reply.decode())

    client_socket.close()