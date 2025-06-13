from Crypto.Cipher import DES, DES3, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

# Ajusta clave e IV a los tamaños requeridos
def adjust_key_iv(key_input, iv_input, key_size, iv_size):
    key = key_input.encode('utf-8')
    iv = iv_input.encode('utf-8')

    if len(key) < key_size:
        key += get_random_bytes(key_size - len(key))
    elif len(key) > key_size:
        key = key[:key_size]

    if len(iv) < iv_size:
        iv += get_random_bytes(iv_size - len(iv))
    elif len(iv) > iv_size:
        iv = iv[:iv_size]

    return key, iv

# Función principal de cifrado y descifrado
def encrypt_decrypt(text, key, iv, algorithm):
    data = text.encode('utf-8')
    cipher = None
    block_size = 8 if algorithm in ['DES', '3DES'] else 16

    if algorithm == 'DES':
        cipher = DES.new(key, DES.MODE_CBC, iv)
    elif algorithm == '3DES':
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
    elif algorithm == 'AES':
        cipher = AES.new(key, AES.MODE_CBC, iv)

    ciphertext = cipher.encrypt(pad(data, block_size))
    cipher_b64 = base64.b64encode(ciphertext)
    cipher_hex = ciphertext.hex()

    # Descifrado
    if algorithm == 'DES':
        cipher_dec = DES.new(key, DES.MODE_CBC, iv)
    elif algorithm == '3DES':
        cipher_dec = DES3.new(key, DES3.MODE_CBC, iv)
    elif algorithm == 'AES':
        cipher_dec = AES.new(key, AES.MODE_CBC, iv)

    decrypted = unpad(cipher_dec.decrypt(ciphertext), block_size)

    return cipher_b64.decode(), cipher_hex, decrypted.decode()

# Diccionario con tamaños por algoritmo
algorithms = {
    "DES": (8, 8),
    "3DES": (24, 8),
    "AES": (32, 16)
}

# Solicitud desde terminal
algorithm = input("Ingrese algoritmo (DES, 3DES, AES): ").strip().upper()
key_input = input("Ingrese clave: ")
iv_input = input("Ingrese IV: ")
text = input("Ingrese texto a cifrar: ")

# Validación
if algorithm not in algorithms:
    print("Algoritmo no soportado.")
    exit()

key_size, iv_size = algorithms[algorithm]
key, iv = adjust_key_iv(key_input, iv_input, key_size, iv_size)
cipher_text,cipher_text_hex, plain_text = encrypt_decrypt(text, key, iv, algorithm)

print(f"\nAlgoritmo: {algorithm}")
print(f"Clave final (hex): {key.hex()}")
print(f"IV final (hex): {iv.hex()}")
print(f"Texto cifrado (base64): {cipher_text}")
print(f"Texto descifradocifrado (hex): {cipher_text_hex}")
print(f"Texto descifrado: {plain_text}")
