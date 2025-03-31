import socket
import time

# Variables
PACKET_SIZE = 1024
SEQ_ID_SIZE = 4
MESSAGE_SIZE = PACKET_SIZE - SEQ_ID_SIZE
timeout = 0.3
receiver_address = ("localhost", 5001)
file_path = "file.mp3"
sender_address = ("0.0.0.0", 5002)

# Read file into chunks
f = open(file_path, "rb")
data = f.read()
chunks = [data[i:i+MESSAGE_SIZE] for i in range(0, len(data), MESSAGE_SIZE)]
f.close()

# Create packets with sequence IDs
packets = []
for i, chunk in enumerate(chunks):
    seq_id_bytes = int.to_bytes(i * MESSAGE_SIZE, SEQ_ID_SIZE, signed=True, byteorder='big')
    packets.append(seq_id_bytes + chunk)

# Create and bind socket
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.bind(sender_address)
sender_socket.settimeout(timeout)

expected_ack_id = 0
total_bytes_sent = 0
packet_delays = []
start_time = time.time()

# Send packets using Stop-and-Wait
for seq_id, packet in enumerate(packets):
    send_time = time.time()
    while True:
        sender_socket.sendto(packet, receiver_address)
        print(f"Sent packet {seq_id}")
        total_bytes_sent += len(packet)
        try:
            ack_packet, _ = sender_socket.recvfrom(PACKET_SIZE)
            ack_id = int.from_bytes(ack_packet[:SEQ_ID_SIZE], signed=True, byteorder='big')
            print(f"Received ACK {ack_id}")
            if ack_id == expected_ack_id + len(packet[SEQ_ID_SIZE:]):
                expected_ack_id = ack_id
                packet_delays.append(time.time() - send_time)
                break
        except socket.timeout:
            print(f"Timeout! Retransmitting packet {seq_id}")

# Send empty message to indicate completion
final_seq_id = int.to_bytes(expected_ack_id, SEQ_ID_SIZE, signed=True, byteorder='big')
sender_socket.sendto(final_seq_id + b'', receiver_address)

# Wait for final ACK and FIN
retry_limit = 5
retry_count = 0
while retry_count < retry_limit:
    try:
        fin_packet, _ = sender_socket.recvfrom(PACKET_SIZE)
        fin_msg = fin_packet[SEQ_ID_SIZE:].decode()
        if "fin" in fin_msg:
            sender_socket.sendto(b'==FINACK==', receiver_address)
            print("Sent FINACK. Transfer complete!")
            break
    except socket.timeout:
        retry_count += 1

total_time = time.time() - start_time
throughput = total_bytes_sent / total_time if total_time > 0 else 0
avg_packet_delay = sum(packet_delays) / len(packet_delays) if packet_delays else float('inf')

# Print results
print(f"Throughput: {throughput:.7f}")
print(f"Average per-packet delay: {avg_packet_delay:.7f}")
print(f"Performance Metric: {0.3*(throughput/1000) + 0.7/(avg_packet_delay if avg_packet_delay > 0 else float('inf')):.7f}")

# Close socket
sender_socket.close()
