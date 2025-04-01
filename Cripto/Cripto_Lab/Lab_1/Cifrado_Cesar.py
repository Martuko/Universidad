def cifrar_cesar(texto, desplazamiento):
    alfabeto_espanol = 'abcdefghijklmnñopqrstuvwxyz'  # Alfabeto español con la ñ
    texto_cifrado = []

    for char in texto:
        if char.isalpha():  # Verificamos si es una letra
            es_mayuscula = char.isupper()  # Verificar si la letra es mayúscula
            char = char.lower()  # Convertimos a minúscula para hacer el cálculo

            if char in alfabeto_espanol:  # Solo procesamos letras dentro del alfabeto
                index = alfabeto_espanol.index(char)
                # Aplicamos el desplazamiento, teniendo en cuenta el alfabeto con la ñ
                nuevo_index = (index + desplazamiento) % len(alfabeto_espanol)
                nuevo_char = alfabeto_espanol[nuevo_index]
                # Convertimos de nuevo a mayúscula si la letra original lo era
                texto_cifrado.append(nuevo_char.upper() if es_mayuscula else nuevo_char)
            else:
                # Si el carácter no está en el alfabeto (como espacios o puntuación), lo agregamos tal cual
                texto_cifrado.append(char)
        else:
            # Si el carácter no es alfabético, lo agregamos tal cual
            texto_cifrado.append(char)

    # Convertimos la lista a un string y lo devolvemos
    return ''.join(texto_cifrado)

# Solicitar los parámetros al usuario
texto_original = input("Ingrese el texto a cifrar: ")
desplazamiento = int(input("Ingrese el valor de desplazamiento: "))

# Obtener y mostrar el texto cifrado
texto_resultado = cifrar_cesar(texto_original, desplazamiento)
print("Texto cifrado:", texto_resultado)
