import numpy as np
import matplotlib.pyplot as plt

# Parámetros iniciales
tiempo_periodico = np.linspace(0, 5, 1000, endpoint=False)  # Tiempo para señales periódicas
tiempo_aperiodico = np.linspace(-1, 2, 1000)  # Tiempo para señales aperiodicas
dt_periodico = tiempo_periodico[1] - tiempo_periodico[0]  # Diferencial de tiempo para señales periódicas
dt_aperiodico = tiempo_aperiodico[1] - tiempo_aperiodico[0]  # Diferencial de tiempo para señales aperiodicas

# Funciones para calcular energía y potencia media
def calcular_energia(signal, dt):
    return np.sum(signal**2) * dt

def calcular_potencia_media(signal):
    return np.mean(signal**2)

# Señales periódicas
# Parámetros para señales periódicas
frecuencia = 2 * np.pi  # Frecuencia angular de 2*pi
desfase = np.pi / 4     # Desfase de pi/4 radianes

senoidal = np.sin(frecuencia * tiempo_periodico + desfase)
cuadrada = np.sign(np.sin(frecuencia * tiempo_periodico + desfase))
triangular = 2 * (tiempo_periodico % 1) - 1
diente_de_sierra = 2 * (tiempo_periodico % 1) - 1

# Cálculo de energía y potencia para señales periódicas
energia_senoidal = calcular_energia(senoidal, dt_periodico)
potencia_senoidal = calcular_potencia_media(senoidal)

energia_cuadrada = calcular_energia(cuadrada, dt_periodico)
potencia_cuadrada = calcular_potencia_media(cuadrada)

energia_triangular = calcular_energia(triangular, dt_periodico)
potencia_triangular = calcular_potencia_media(triangular)

energia_diente_de_sierra = calcular_energia(diente_de_sierra, dt_periodico)
potencia_diente_de_sierra = calcular_potencia_media(diente_de_sierra)

# Señales aperiodicas
# Exponencial decreciente (un tramo)
exponencial_decreciente = np.exp(-tiempo_aperiodico) * (tiempo_aperiodico >= 0) * (tiempo_aperiodico < 1)

# Exponencial creciente (un tramo)
exponencial_creciente = np.exp(tiempo_aperiodico) * (tiempo_aperiodico >= 0) * (tiempo_aperiodico < 1)

# Impulso (aproximación)
impulso = np.zeros_like(tiempo_aperiodico)
impulso[np.abs(tiempo_aperiodico) < dt_aperiodico] = 1 / dt_aperiodico  # Aproximación del delta de Dirac

# Escalón
escalon = np.heaviside(tiempo_aperiodico, 1)

# Sinc
sinc = np.sinc(tiempo_aperiodico)  # Sinc es sen(t)/t

# Cálculo de energía y potencia para señales aperiodicas
energia_exponencial_decreciente = calcular_energia(exponencial_decreciente, dt_aperiodico)
potencia_exponencial_decreciente = calcular_potencia_media(exponencial_decreciente)

energia_exponencial_creciente = calcular_energia(exponencial_creciente, dt_aperiodico)
potencia_exponencial_creciente = calcular_potencia_media(exponencial_creciente)

energia_impulso = calcular_energia(impulso, dt_aperiodico)
potencia_impulso = calcular_potencia_media(impulso)

energia_escalon = calcular_energia(escalon, dt_aperiodico)
potencia_escalon = calcular_potencia_media(escalon)

energia_sinc = calcular_energia(sinc, dt_aperiodico)
potencia_sinc = calcular_potencia_media(sinc)

# Imprimir resultados
print("Energía y Potencia de las señales periódicas:")
print(f"Senoidal: Energía = {energia_senoidal:.4f}, Potencia Media = {potencia_senoidal:.4f}")
print(f"Cuadrada: Energía = {energia_cuadrada:.4f}, Potencia Media = {potencia_cuadrada:.4f}")
print(f"Triangular: Energía = {energia_triangular:.4f}, Potencia Media = {potencia_triangular:.4f}")
print(f"Diente de Sierra: Energía = {energia_diente_de_sierra:.4f}, Potencia Media = {potencia_diente_de_sierra:.4f}")

print("\nEnergía y Potencia de las señales aperiodicas:")
print(f"Exponencial Decreciente: Energía = {energia_exponencial_decreciente:.4f}, Potencia Media = {potencia_exponencial_decreciente:.4f}")
print(f"Exponencial Creciente: Energía = {energia_exponencial_creciente:.4f}, Potencia Media = {potencia_exponencial_creciente:.4f}")
print(f"Impulso: Energía = {energia_impulso:.4f}, Potencia Media = {potencia_impulso:.4f}")
print(f"Escalón: Energía = {energia_escalon:.4f}, Potencia Media = {potencia_escalon:.4f}")
print(f"Sinc: Energía = {energia_sinc:.4f}, Potencia Media = {potencia_sinc:.4f}")
