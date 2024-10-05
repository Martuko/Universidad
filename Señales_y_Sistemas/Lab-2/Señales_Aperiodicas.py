import numpy as np
import matplotlib.pyplot as plt

# Parámetros iniciales
tiempo = np.linspace(0, 5, 1000, endpoint=False)  # Tiempo de 0 a 5 segundos

# Señales aperiódicas
# Exponencial decreciente
exp_decreciente = np.exp(-tiempo) * (tiempo >= 0) * (tiempo <= 1)

# Exponencial creciente
exp_creciente = np.exp(tiempo) * (tiempo >= 0) * (tiempo <= 1)

# Impulso
impulso = np.zeros_like(tiempo)
impulso[0] = 1  # Definimos el impulso en t=0

# Escalón
escalon = np.heaviside(tiempo, 1)  # Heaviside es la función escalón

# Sinc
sinc = np.sinc(tiempo / np.pi)  # np.sinc normalizado

# Función para graficar señales individualmente con ajuste de ejes
def graficar_senales(t, senal, titulo):
    plt.figure(figsize=(10, 6))
    plt.plot(t, senal)
    plt.title(titulo)
    plt.xlim(0, 5)  # Rango de 0 a 5 en el eje X
    plt.ylim(-0.5, 1.5)  # Rango ajustado en el eje Y
    plt.xticks(np.arange(0, 6, 1))  # Incrementos de 1 en el eje X
    plt.yticks(np.arange(-0.5, 1.75, 0.25))  # Incrementos de 0.25 en el eje Y
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()

# Lista de señales y títulos
senales = [exp_decreciente, exp_creciente, impulso, escalon, sinc]
titulos = ['Exponencial Decreciente', 'Exponencial Creciente', 'Impulso', 'Escalón', 'Sinc']

# Graficar cada señal una por una
for senal, titulo in zip(senales, titulos):
    graficar_senales(tiempo, senal, titulo)
