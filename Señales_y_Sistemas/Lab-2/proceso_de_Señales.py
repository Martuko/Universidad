import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

# Definir el intervalo de tiempo
t = np.linspace(0, 1, 500, endpoint=False)

# Señales periódicas
senoidal = np.sin(2 * np.pi * 5 * t)
cuadrada = np.sign(np.sin(2 * np.pi * 2 * t))
triangular = np.abs((t * 4 % 4 - 2) - 1) - 1
diente_de_sierra = t * 2 % 2 - 1

# Señales aperiódicas
exponencial_decreciente = np.exp(-t) * (t <= 1)
exponencial_creciente = np.exp(t) * (t <= 1)
impulso = np.where(t == 0, 1, 0)  # Aproximación de un impulso en t=0
escalon = t > 0

# Función para graficar señales
def plot_signal(time, signal, title):
    plt.figure(figsize=(10, 2))
    plt.plot(time, signal)
    plt.title(title)
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()

# Graficar las señales periódicas y aperiódicas
signals = [senoidal, cuadrada, triangular, diente_de_sierra, exponencial_decreciente, exponencial_creciente, impulso, escalon]
titles = ['Señal Senoidal', 'Señal Cuadrada', 'Señal Triangular', 'Señal Diente de Sierra', 
          'Exponencial Decreciente', 'Exponencial Creciente', 'Impulso', 'Escalón']

for signal, title in zip(signals, titles):
    plot_signal(t, signal, title)

# Ejemplo de convolución: Convolver una señal senoidal con una exponencial decreciente
output_conv = convolve(senoidal, exponencial_decreciente, mode='same')

# Graficar la convolución
plot_signal(t, output_conv, 'Resultado de la Convolución Senoidal y Exponencial Decreciente')

# Realizar más convoluciones si es necesario
# Añadir más convoluciones y análisis según las instrucciones del laboratorio
