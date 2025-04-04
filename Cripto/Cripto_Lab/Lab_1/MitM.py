import difflib
from scapy.all import rdpcap, ICMP
from termcolor import colored

def extraer_mensaje_icmp(archivo_pcap):
    paquetes = rdpcap(archivo_pcap)
    mensaje = ""
    for pkt in paquetes:
        if ICMP in pkt and pkt[ICMP].type == 8:
            try:
                carga = pkt[ICMP].payload.load.decode("utf-8")
                mensaje += carga.strip()
            except:
                continue
    return mensaje

def descifrar_cesar(texto, desplazamiento):
    alfabeto = "abcdefghijklmnñopqrstuvwxyz"
    resultado = []
    for char in texto:
        if char.isalpha():
            es_mayus = char.isupper()
            char = char.lower()
            if char in alfabeto:
                nuevo_char = alfabeto[(alfabeto.index(char) - desplazamiento) % len(alfabeto)]
                resultado.append(nuevo_char.upper() if es_mayus else nuevo_char)
            else:
                resultado.append(char)
        else:
            resultado.append(char)
    return ''.join(resultado)

def cargar_diccionario(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        return [palabra.strip().lower() for palabra in f if palabra.strip()]

def mejor_coincidencia(texto, diccionario):
    mejores = difflib.get_close_matches(texto, diccionario, n=1, cutoff=0.5)
    if mejores:
        ratio = difflib.SequenceMatcher(None, texto, mejores[0]).ratio()
        return mejores[0], ratio
    return None, 0.0

def main():
    print("Ingrese el nombre del archivo .pcapng:", end=" ")
    archivo_pcap = input().strip()
    mensaje_cifrado = extraer_mensaje_icmp(archivo_pcap)
    print(f"\nMensaje cifrado extraído: {mensaje_cifrado}")

    diccionario = cargar_diccionario("palabras.txt")
    print(f"\nPalabras en el diccionario: {len(diccionario)}")
    print("\nProbando todos los desplazamientos posibles...\n")

    mejor_texto = ""
    mejor_desplazamiento = 0
    mejor_puntaje = 0.0
    mejor_palabra = ""

    resultados = []

    for desplazamiento in range(1, len("abcdefghijklmnñopqrstuvwxyz")):
        descifrado = descifrar_cesar(mensaje_cifrado, desplazamiento)
        palabra_similar, puntaje = mejor_coincidencia(descifrado, diccionario)
        resultados.append((desplazamiento, descifrado, puntaje, palabra_similar))

        if puntaje > mejor_puntaje:
            mejor_texto = descifrado
            mejor_desplazamiento = desplazamiento
            mejor_puntaje = puntaje
            mejor_palabra = palabra_similar

    # Mostrar resultados
    for desplazamiento, texto, puntaje, _ in resultados:
        if desplazamiento == mejor_desplazamiento:
            print(colored(f"✅ Desplazamiento: {desplazamiento} - Texto: {texto} - Puntuación: {puntaje:.2f}", "green"))
        else:
            print(f"Desplazamiento: {desplazamiento} - Texto: {texto} - Puntuación: {puntaje:.2f}")

    # Resultado final
    print("\nResultado más probable:")
    print(colored(f"✔ Desplazamiento: {mejor_desplazamiento}", "green"))
    print(colored(f"✔ Texto descifrado: {mejor_texto}", "green"))
    print(colored(f"✔ Puntuación de similitud: {mejor_puntaje:.2f}", "green"))
    if mejor_palabra:
        print(colored(f"✔ Palabra más parecida en diccionario: {mejor_palabra}", "cyan"))

if __name__ == "__main__":
    main()
