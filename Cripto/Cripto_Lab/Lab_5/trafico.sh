#!/bin/bash

# Uso: ./trafico.sh archivo.pcapng

PCAP="$1"

echo "========== Tamaño de paquetes del flujo =========="
tshark -r "$PCAP" -Y "tcp.port == 22" -T fields -e frame.number -e frame.len -e ip.src -e ip.dst

echo ""
echo "========== Contenido visible en texto plano (si lo hay) =========="
tshark -r "$PCAP" -Y "tcp.port == 22 && data" -T fields -e ip.src -e ip.dst -e data.data
