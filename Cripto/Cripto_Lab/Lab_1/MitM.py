import random
import time
from scapy.all import rdpcap, ICMP
from termcolor import colored

# Lista de palabras comunes en español (puedes ampliar esta lista)
PALABRAS_COMUNES = {
    "el", "la", "de", "y", "que", "en", "a", "los", "del", "se", "con", "por", "las", "un", "una", "para", "es", "al", "como", "su"
}

# Función para cifrar y descifrar con el algoritmo de César (aplicando el desplazamiento negativo)
def descifrar_cesar(texto, desplazamiento):
    texto_descifrado = []
    
    # Alfabeto en español, incluyendo la ñ
    alfabeto_espanol = 'abcdefghijklmnñopqrstuvwxyz'
    
    for char in texto:
        if char.isalpha():
            es_mayuscula = char.isupper()
            char = char.lower()

            if char in alfabeto_espanol:
                index = alfabeto_espanol.index(char)
                nuevo_index = (index - desplazamiento) % len(alfabeto_espanol)  # Desplazamiento negativo
                nuevo_char = alfabeto_espanol[nuevo_index]
                texto_descifrado.append(nuevo_char.upper() if es_mayuscula else nuevo_char)
            else:
                texto_descifrado.append(char)
        else:
            texto_descifrado.append(char)

    return ''.join(texto_descifrado)

# Función para evaluar la probabilidad de un texto basado en palabras comunes
def evaluar_legibilidad(texto):
    puntuacion = 0
    palabras = texto.lower().split()

    # Contamos cuántas palabras del texto están en nuestra lista de palabras comunes
    for palabra in palabras:
        if palabra in PALABRAS_COMUNES:
            puntuacion += 1
    
    return puntuacion

# Función para procesar el archivo pcapng y extraer los datos de los paquetes ICMP
def extraer_datos_icmp(archivo_pcapng):
    paquetes = rdpcap(archivo_pcapng)
    mensaje_cifrado = ""

    for paquete in paquetes:
        if paquete.haslayer(ICMP) and paquete[ICMP].type == 8:  # Echo Request
            # Extraemos el contenido de datos del paquete ICMP
            if paquete[ICMP].payload:
                # Los datos de ICMP son texto, por lo que los convertimos a cadena
                mensaje_cifrado += str(bytes(paquete[ICMP].payload), 'utf-8')

    return mensaje_cifrado

# Función para probar todos los desplazamientos posibles
def probar_descifrado(texto):
    print("Probando todos los desplazamientos posibles...\n")
    mejores_resultados = []
    
    # Probar todos los desplazamientos de 1 a 25
    for i in range(1, 26):
        texto_descifrado = descifrar_cesar(texto, i)
        puntuacion = evaluar_legibilidad(texto_descifrado)
        
        # Guardamos el resultado con la puntuación y el desplazamiento
        mejores_resultados.append((texto_descifrado, puntuacion, i))  # Incluimos el desplazamiento aquí
    
    # Encontramos el descifrado con la puntuación más alta
    mejores_resultados.sort(key=lambda x: x[1], reverse=True)
    mejor_descifrado = mejores_resultados[0]
    
    # Mostrar los resultados en el orden original de desplazamientos
    for desplazamiento in range(1, 26):
        # Encontramos el texto cifrado y la puntuación para el desplazamiento actual
        texto_descifrado, puntuacion, _ = next((r for r in mejores_resultados if r[2] == desplazamiento), (None, None, None))
        
        if puntuacion == mejor_descifrado[1]:  # Destacar el mejor desplazamiento
            print(colored(f"Desplazamiento: {desplazamiento} - {texto_descifrado} (probable)", "green"))
        else:
            print(f"Desplazamiento: {desplazamiento} - {texto_descifrado}")

# Función principal para ejecutar el análisis
def main(archivo_pcapng):
    # Extraemos el mensaje cifrado de los paquetes ICMP
    mensaje_cifrado = extraer_datos_icmp(archivo_pcapng)
    
    if not mensaje_cifrado:
        print("No se encontraron paquetes ICMP con datos para procesar.")
        return
    
    print(f"Mensaje cifrado extraído: {mensaje_cifrado}")
    
    # Probar y mostrar los resultados
    probar_descifrado(mensaje_cifrado)

# Ejecutar el script con el archivo pcapng proporcionado
if __name__ == "__main__":
    archivo_pcapng = input("Ingrese el nombre del archivo .pcapng: ")
    main(archivo_pcapng)
