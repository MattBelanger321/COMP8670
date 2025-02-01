import random
import time
import csv


class TCPTahoe:
    def __init__(self, threshold=16, max_window=64):
        self.cwnd = 1  # Congestion window
        self.ssthresh = threshold  # Slow start threshold
        self.max_window = max_window  # Maximum congestion window size
        self.packets_sent = 0
        self.acks_received = 0
        self.packet_loss_rate = 0.05  # 10% packet loss probability
        self.state = "slow_start"  # Initial state: Slow Start
        log_file = f"./trials/tcp_tahoe_window{max_window}_thresh{
            threshold}_loss{self.packet_loss_rate}_log.csv"
        self.log_file = log_file

        # Initialize log file
        with open(self.log_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Packet", "State", "CWND", "SSTHRESH"])

    def log_state(self):
        """Logs the current state to a CSV file."""
        with open(self.log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.packets_sent, self.state,
                            self.cwnd, self.ssthresh])

    def send_packet(self):
        """Simulates sending packets and handles packet loss."""
        self.packets_sent += 1
        if random.random() < self.packet_loss_rate:
            print(f"Packet {self.packets_sent} lost!")
            self.handle_loss()
        else:
            print(f"Packet {self.packets_sent} sent successfully.")
            self.handle_ack()
        self.log_state()

    def handle_ack(self):
        """Handles an ACK received from the receiver."""
        self.acks_received += 1
        if self.state == "slow_start":
            self.cwnd += 1
            print(f"ACK {self.acks_received} received. State: {
                  self.state}. cwnd: {self.cwnd}, ssthresh: {self.ssthresh}")
            if self.cwnd >= self.ssthresh:
                self.state = "congestion_avoidance"
        elif self.state == "congestion_avoidance":
            self.cwnd += 1 / self.cwnd  # Additive increase
            print(f"ACK {self.acks_received} received. State: {
                  self.state}. cwnd: {self.cwnd:.2f}, ssthresh: {self.ssthresh}")

        # Ensure cwnd doesn't exceed max_window
        self.cwnd = min(self.cwnd, self.max_window)

    def handle_loss(self):
        """Handles packet loss."""
        print(f"Packet loss detected! Reducing ssthresh and resetting cwnd.")
        # Reduce ssthresh to half of cwnd
        self.ssthresh = max(self.cwnd / 2, 2)
        self.cwnd = 1  # Reset cwnd to 1 (slow start)
        self.state = "slow_start"

    def run_simulation(self, rounds=50):
        """Runs the TCP Tahoe simulation for a specified number of rounds."""
        for _ in range(rounds):
            time.sleep(0.1)  # Simulate some delay between packet transmissions
            self.send_packet()


if __name__ == "__main__":
    tcp_tahoe = TCPTahoe(threshold=16, max_window=64)
    tcp_tahoe.run_simulation(rounds=50)
