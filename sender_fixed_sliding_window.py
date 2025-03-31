import socket
import time


WINDOW_SIZE = 100
PACKET_SIZE = 1024  
RECEIVER_IP = "localhost"
RECEIVER_PORT = 5001


sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_socket.settimeout(2)  


with open("file.mp3", "rb") as f:
    data = f.read()

packets = [data[i:i + PACKET_SIZE] for i in range(0, len(data), PACKET_SIZE)]
total_packets = len(packets)

base = 0
next_seq = 0
window = {}

start_time = time.time()
packet_delays = {}

while base < total_packets:
    while next_seq < base + WINDOW_SIZE and next_seq < total_packets:
        packet_data = packets[next_seq]
        seq_id = next_seq
        packet = seq_id.to_bytes(4, 'big', signed=True) + packet_data
        timestamp = time.time()
        sender_socket.sendto(packet, (RECEIVER_IP, RECEIVER_PORT))
        
        print(f"Sent packet {next_seq}") 
        
        #store timestamp for delay calculation
        packet_delays[next_seq] = timestamp
        window[next_seq] = packet  # store packet for retransmission
        next_seq += 1

    try:
        # wait for ACKs
        ack_data, _ = sender_socket.recvfrom(1024)
        ack_seq_id = int.from_bytes(ack_data[:4], 'big', signed=True) 
        print(f"Received ACK {ack_seq_id}")  

        #move the window forward
        if ack_seq_id >= base:
            for i in range(base, ack_seq_id + 1):
                if i in packet_delays:
                    packet_delays[i] = time.time() - packet_delays[i]  # Compute delay
                if i in window:
                    del window[i]
            base = ack_seq_id + 1  #slide the window

    except socket.timeout:
        #retransmit all unacknowledged packets if timeout occurs
        print(f"Timeout! Resending from packet {base}")  # Debug
        for i in range(base, next_seq):
            sender_socket.sendto(window[i], (RECEIVER_IP, RECEIVER_PORT))
            print(f"Resent packet {i}")

#send empty message to indicate completion
sender_socket.sendto(b"==FINACK==", (RECEIVER_IP, RECEIVER_PORT))
print("Finished sending")

#compute throughput and delay
end_time = time.time()
throughput = len(data) / (end_time - start_time)
avg_delay = sum(packet_delays.values()) / len(packet_delays)
 
print(f"Throughput: {throughput:.7f}")
print(f"Avg. Delay: {avg_delay:.7f}")
print(f"Performance: {0.3*(throughput / 100) + 0.7/avg_delay:.7f}")  # Example performance metric

sender_socket.close()
