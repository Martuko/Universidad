#!/bin/bash
PCAP="$1"

echo "========== Tamaño de paquetes del flujo =========="
tshark -r "$PCAP" -Y "tcp.port == 22" -T fields -e frame.number -e frame.len -e ip.src -e ip.dst

echo ""

