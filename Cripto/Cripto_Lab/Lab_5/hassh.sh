#!/bin/bash

PCAP="$1"

ALGORITHMS=$(tshark -r "$PCAP" -Y "ssh.kex_algorithms && ip.src==192.168.200.4" -T fields -e ssh.kex.hassh_algorithms)
HASH=$(tshark -r "$PCAP" -Y "ssh.kex_algorithms && ip.src==192.168.200.4" -T fields -e ssh.kex.hassh)

echo "HASSH Algorithms:"
echo "$ALGORITHMS"
echo "HASSH MD5:"
echo "$HASH"
