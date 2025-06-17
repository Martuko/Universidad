#!/bin/bash

PCAP="$1"

FIELDS=$(tshark -r "$PCAP" -Y "ssh.kex_algorithms && ip.src==192.168.200.5" -T fields \
  -e ssh.kex_algorithms \
  -e ssh.server_host_key_algorithms \
  -e ssh.encryption_algorithms_client_to_server \
  -e ssh.mac_algorithms_client_to_server \
  -e ssh.compression_algorithms_client_to_server)

HASSH_STRING=$(echo "$FIELDS" | paste -sd ";" -)
echo "HASSH String:"
echo "$HASSH_STRING"
echo -n "$HASSH_STRING" | md5sum

