import numpy as np
import matplotlib.pyplot as plt

# Parámetros iniciales
tiempo = np.linspace(0, 1, 1000, endpoint=False)

# Señales periódicas
senoidal = np.sin(2 * np.pi * 5 * tiempo)
cuadrada = np.sign(np.sin(2 * np.pi * 2 * tiempo))
triangular = np.abs((tiempo * 4 % 4 - 2) - 1) - 1
diente_de_sierra = np.remainder(tiempo * 2, 2) - 1

# Señales aperiódicas
exp_decreciente = np.exp(-tiempo) * (tiempo <= 1)
exp_creciente = np.exp(tiempo) * (tiempo <= 1)
impulso = np.where(tiempo == 0, 1, 0)
escalon = tiempo >= 0

# Función para graficar señales
def graficar_senales(t, senales, titulos):
    plt.figure(figsize=(10, 12))
    for i, (senal, titulo) in enumerate(zip(senales, titulos), 1):
        plt.subplot(len(senales), 1, i)
        plt.plot(t, senal, label=titulo)
        plt.title(titulo)
        plt.grid(True)
    plt.tight_layout()
    plt.show()

# Lista de señales y títulos
senales = [senoidal, cuadrada, triangular, diente_de_sierra, exp_decreciente, exp_creciente, impulso, escalon]
titulos = ['Senoidal', 'Cuadrada', 'Triangular', 'Diente de Sierra', 'Exponencial Decreciente', 'Exponencial Creciente', 'Impulso', 'Escalón']

# Graficar todas las señales
graficar_senales(tiempo, senales, titulos)
