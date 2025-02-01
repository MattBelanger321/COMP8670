import random
import time
import csv
import os


class TCPReno:
    def __init__(self, threshold=16, max_window=64):
        self.cwnd = 1  # Congestion window
        self.ssthresh = threshold  # Slow start threshold
        self.max_window = max_window  # Maximum congestion window size
        self.packets_sent = 0
        self.acks_received = 0
        self.packet_loss_rate = 0.2  # packet loss probability
        self.state = "slow_start"  # Initial state: Slow Start
        self.dup_acks = 0.5  # Duplicate ACK probability

        # Create trials directory if it doesn't exist
        os.makedirs("./trials", exist_ok=True)

        # Initialize log file
        self.log_file = f"./trials/tcp_reno_window{max_window}_thresh{
            threshold}_loss{self.packet_loss_rate}_log.csv"
        with open(self.log_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Packet", "State", "CWND", "SSTHRESH"])

    def log_state(self):
        """Logs the current state to a CSV file."""
        with open(self.log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.packets_sent,
                self.state,
                round(self.cwnd, 2),
                round(self.ssthresh, 2)
            ])

    def send_packet(self):
        """
        Simulates sending packets and handles packet loss.
        Returns True if packet was sent successfully, False otherwise.
        """
        self.packets_sent += 1

        if random.random() < self.packet_loss_rate:
            print(f"Packet {self.packets_sent} lost!")
            self.handle_loss()
            return False
        else:
            print(f"Packet {self.packets_sent} sent successfully.")
            self.handle_ack()
            self.log_state()
            return True

    def handle_ack(self):
        """Handles an ACK received from the receiver."""
        self.acks_received += 1

        if self.state == "slow_start":
            self.cwnd += 1
            print(f"ACK {self.acks_received} received. "
                  f"State: {self.state}. "
                  f"cwnd: {self.cwnd}, ssthresh: {self.ssthresh}")

            if self.cwnd >= self.ssthresh:
                self.state = "congestion_avoidance"

        elif self.state == "congestion_avoidance":
            # Additive increase: increase cwnd by 1/cwnd
            self.cwnd += 1 / self.cwnd
            print(f"ACK {self.acks_received} received. "
                  f"State: {self.state}. "
                  f"cwnd: {self.cwnd:.2f}, ssthresh: {self.ssthresh}")

        elif self.state == "fast_recovery":
            # Fast recovery: Increase cwnd by 1 for each additional ACK
            self.cwnd += 1
            print(f"Fast Recovery: ACK {self.acks_received} received. "
                  f"cwnd: {self.cwnd}, ssthresh: {self.ssthresh}")

            # Exit fast recovery if we receive an ACK for the retransmitted packet
            if random.random() < 0.3:  # 30% chance to exit fast recovery
                self.state = "congestion_avoidance"
                self.cwnd = self.ssthresh
                print("Exiting Fast Recovery")

        # Ensure cwnd doesn't exceed max_window
        self.cwnd = min(self.cwnd, self.max_window)

    def handle_loss(self):
        """Handles packet loss using either Fast Recovery or Slow Start."""
        print("Packet loss detected! Triggering Fast Recovery or Slow Start.")

        if random.random() < self.dup_acks:
            # Fast Recovery
            print("Entering Fast Recovery!")
            self.ssthresh = max(self.cwnd / 2, 2)
            self.cwnd = self.ssthresh + 3  # After three duplicate ACKs
            self.state = "fast_recovery"
        else:
            # Standard loss: Slow Start (Tahoe-style)
            self.ssthresh = max(self.cwnd / 2, 2)
            self.cwnd = 1
            self.state = "slow_start"

    def run_simulation(self, rounds=50):
        """
        Runs the TCP Reno simulation for a specified number of rounds.

        Args:
            rounds (int): Number of simulation rounds to run
        """
        print(f"\nStarting TCP Reno simulation for {rounds} rounds...")
        print(f"Initial settings: threshold={
              self.ssthresh}, max_window={self.max_window}")
        print(f"Packet loss rate: {self.packet_loss_rate*100}%")
        print("-" * 50)

        for round_num in range(rounds):
            print(f"\nRound {round_num + 1}/{rounds}")
            time.sleep(0.1)  # Simulate network delay
            self.send_packet()

        print("\nSimulation complete!")
        print(f"Total packets sent: {self.packets_sent}")
        print(f"Total ACKs received: {self.acks_received}")
        print(f"Packet loss rate: {
              (self.packets_sent - self.acks_received) / self.packets_sent:.2%}")
        print(f"Results logged to: {self.log_file}")


if __name__ == "__main__":
    tcp_reno = TCPReno(threshold=16, max_window=64)
    tcp_reno.run_simulation(rounds=50)
