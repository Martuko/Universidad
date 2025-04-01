import random
import time
from scapy.all import ICMP, IP, send

# Función para enviar un paquete ICMP con un solo carácter
def enviar_paquete_icmp(destino, mensaje):
    # Construimos el paquete ICMP con el mensaje
    paquetes_enviados = []
    for char in mensaje:
        # Construcción de la IP de destino (realmente puede ser cualquier IP)
        ip_paquete = IP(dst=destino)
        
        # Paquete ICMP con el carácter como datos
        paquete_icmp = ICMP(type='echo-request')/char
        
        # Enviar el paquete
        send(ip_paquete/paquete_icmp, verbose=False)
        paquetes_enviados.append(f"Paquete con '{char}' enviado.")
        
        # Aleatorización en el intervalo entre paquetes (entre 0.05 y 0.2 segundos)
        time.sleep(random.uniform(0.05, 0.2))
    
    return paquetes_enviados

# Función para demostrar la simulación con comparación de tráfico
def comparar_trafico(mensaje):
    destino = "8.8.8.8"  # Dirección IP de destino, puede ser cualquier IP
    print(f"Enviando tráfico ICMP para el mensaje: '{mensaje}'\n")
    paquetes_enviados = enviar_paquete_icmp(destino, mensaje)
    for paquete in paquetes_enviados:
        print(paquete)

# Solicitar al usuario el mensaje a enviar
mensaje = input("Ingrese el mensaje a enviar (como texto): ")

# Llamada a la función de comparación y envío de tráfico ICMP
comparar_trafico(mensaje)
