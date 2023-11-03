import socket
import time

# specify host and port to receive messages on
HOST = '127.0.0.1'
PORT = 5500

DATASIZE = 1024 * 100

# create a new datagram socket
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    # bind this socket to OS
    server_socket.bind((HOST, PORT))

    print("Server listening to port: 5500...")
    total_size = 0
    total_time = 0
    # receive messages indefinitely
    while True:
        # Get starting time
        initial_time = time.time()

        # Catch data sent from clients
        data, addr = server_socket.recvfrom(1024)

        # Get ending time
        final_time = time.time()

        # Keeping track of packets size and the time taken to receive
        # them
        total_size += len(data)
        total_time += final_time - initial_time

        if total_size == DATASIZE:
            # Computer the thoughput
            throughput = (total_size / 1024) / total_time

            # Sending computed throughput to client
            server_socket.sendto(str(throughput).encode(), addr)

            server_socket.close()

