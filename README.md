# UDP Sender Implementation with Congestion Control Protocols

## Project Overview
This project involves developing a UDP sender in Python to transmit a large file (`file.mp3`) from a Docker container to a UDP receiver. The sender must handle packet-based transmission under an emulated network profile, which introduces delays, sets buffer sizes, and determines link throughput.

## Implementation Details
The sender will be implemented using three different congestion control protocols:

1. **Stop-and-Wait Protocol** – Ensures reliable transmission by waiting for an acknowledgment before sending the next packet.  
2. **Fixed Sliding Window Protocol (Window Size = 100)** – Allows up to 100 packets to be in transit before requiring acknowledgment.  
3. **TCP Reno (Extra Credit)** – Implements congestion control with slow start, congestion avoidance, and fast retransmit.

Each sender must:
- Transmit data in **1024-byte packets**.
- Track **sequence numbers** to ensure correct packet ordering.
- Measure and report **throughput** (bytes per second).
- Calculate **per-packet delay** (time between sending and receiving acknowledgment).
- Compute a **performance metric** to evaluate efficiency.

## Performance Metric Formula
The performance of the UDP sender is evaluated using the following formula:

$$
\text{Metric} = 0.3 \times \frac{\text{Throughput}}{1000} + \frac{0.7}{\text{Average delay per packet}}
$$

where:
- **Throughput** is measured in bytes per second.
- **Average delay per packet** is measured in seconds.

## Output
- A **final output** with only three lines per run:
  - Throughput (bytes per second)
  - Per-packet delay (seconds)
  - Performance metric

## How to Run
### Docker is needed for this project
1. From the ```docker``` directory, run ```./start-simulator.sh``` to start running the receiver.py file with the emulated network profile. Once it's running successfully, you will see a message saying Receiver running.
2. The receiver has already been programmed to send acknowledgements to the sender similar to the receiver in the discussion.
3. Run ```python3 sender_stop_and_wait.py``` for the stop-and-wait protocol
4. Run ```python3 sender_fixed_sliding_window.py``` for the fixed sliding window protocol
