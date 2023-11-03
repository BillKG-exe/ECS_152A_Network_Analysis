import socket
import time

# Server configuration
host = '127.0.0.1'
port = 5500  

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the host and port
server_socket.bind((host, port))
print("Sever listening to port: 5500...")

data_received = b''  # Initialize an empty byte string to store received data

start_time = time.time()  # Start time for measuring throughput

try:
    while True:
        # Receive data in smaller chunks
        chunk, client_address = server_socket.recvfrom(1024)  # Adjust chunk size if needed
        data_received += chunk

        if len(data_received) == 1024 * 100:
            break
except socket.timeout:
    pass

end_time = time.time()  # End time for measuring throughput
server_socket.close()

# Calculate throughput in kilobytes per second
data_received_size = len(data_received) / 1024  # Convert to kilobytes
time_taken = end_time - start_time
throughput = data_received_size / time_taken

# Send the throughput value back to the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto(str(throughput).encode(), client_address)