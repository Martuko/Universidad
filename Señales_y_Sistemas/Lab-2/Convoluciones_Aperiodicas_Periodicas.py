import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import sawtooth

# Parámetros iniciales
tiempo = np.linspace(0, 2, 1000, endpoint=False)  # Tiempo de 0 a 2 segundos (para ver mejor las señales)
frecuencia = 5 * np.pi  # Aumentar la frecuencia para períodos más cortos
desfase = 0  # Desfase de 0 radianes

# Creación de señales periódicas
# Señal senoidal
senoidal = np.sin(frecuencia * tiempo + desfase)

# Señal cuadrada
cuadrada = np.sign(np.sin(frecuencia * tiempo + desfase))

# Señal diente de sierra
diente_de_sierra = sawtooth(frecuencia * tiempo + desfase)

# Señal triangular (creación manual)
def crear_señal_triangular(tiempo):
    return 2 * (tiempo % 0.2) / 0.2 - 1  # Normalizada a [-1, 1], ciclo cada 0.2s

triangular = crear_señal_triangular(tiempo)

# Creación de señales aperiódicas
# Exponencial decreciente
exp_decreciente = np.exp(-tiempo) * (tiempo >= 0) * (tiempo <= 1)

# Exponencial creciente
exp_creciente = np.exp(tiempo) * (tiempo >= 0) * (tiempo <= 1)

# Impulso
impulso = np.zeros_like(tiempo)
impulso[0] = 1  # Definimos el impulso en t=0

# Escalón
escalon = np.heaviside(tiempo, 1)  # Heaviside es la función escalón

# Función para realizar la convolución y graficar los resultados
def graficar_convolucion(tiempo1, tiempo2, señal1, señal2, titulo):
    convolucion = np.convolve(señal1, señal2, mode='full')
    tiempo_convolucion = np.linspace(0, tiempo1[-1] + tiempo2[-1], len(convolucion))

    plt.figure(figsize=(12, 6))
    plt.plot(tiempo_convolucion, convolucion)
    plt.title(titulo)
    plt.xlim(0, 5)  # Limitar el eje X de 0 a 5 segundos
    plt.ylim(min(convolucion), max(convolucion))  # Ajustar el eje Y según la convolución
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()

# Convoluciones
graficar_convolucion(tiempo, tiempo, impulso, senoidal, 'Convolución de Señal Impulso con Senoidal')
graficar_convolucion(tiempo, tiempo, exp_decreciente, triangular, 'Convolución de Señal Exponencial Decreciente con Triangular')
graficar_convolucion(tiempo, tiempo, exp_creciente, cuadrada, 'Convolución de Señal Exponencial Creciente con Cuadrada')
graficar_convolucion(tiempo, tiempo, escalon, diente_de_sierra, 'Convolución de Señal Escalón con Diente de Sierra')
