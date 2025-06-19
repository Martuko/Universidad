#!/bin/bash
PCAP="$1"

echo "========== Tamaño de paquetes del flujo =========="
tshark -r "$PCAP" -Y "tcp.port == 22" -T fields -e frame.number -e ip.src -e ip.dst -e ssh.protocol 

echo ""

