import socket

# Client configuration
host = '127.0.0.1'
port = 5500  
data_to_send = b'A' * (1024 * 100)  # Create 100 KB of data

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send data in smaller chunks
chunk_size = 1024  

for i in range(0, len(data_to_send), chunk_size):
    chunk = data_to_send[i:i + chunk_size]
    client_socket.sendto(chunk, (host, port))

# Wait for the server to respond with the throughput
throughput, server_address = client_socket.recvfrom(1024)  # Adjust buffer size if needed

# Print the received throughput on the client side
print(f"Client Received Throughput: {throughput.decode()} KB/s")

client_socket.close()
