import numpy as np
import matplotlib.pyplot as plt

# Parámetros iniciales
tiempo = np.linspace(0, 5, 1000, endpoint=False)  # Tiempo de 0 a 5 segundos
frecuencia = 2 * np.pi  # Frecuencia angular de 2*pi
desfase = np.pi / 4     # Desfase de pi/4 radianes

# Señales periódicas con frecuencia y desfase aplicados
senoidal = np.sin(frecuencia * tiempo + desfase)
cuadrada = np.sign(np.sin(frecuencia * tiempo + desfase))
triangular = np.abs((frecuencia * tiempo + desfase) % 4 - 2) - 1
diente_de_sierra = (frecuencia * tiempo + desfase) % 2 - 1

# Función para graficar señales individualmente con ajuste de ejes
def graficar_senales(t, senal, titulo):
    plt.figure(figsize=(10, 6))  # Aumentar el alto del gráfico
    plt.plot(t, senal)
    plt.title(titulo)
    plt.xlim(0, 5)  # Rango de 0 a 5 en el eje X
    plt.ylim(-1, 1)  # Rango de -1 a 1 en el eje Y
    plt.xticks(np.arange(0, 6, 1))  # Incrementos de 1 en el eje X
    plt.yticks(np.arange(-1, 1.25, 0.25))  # Incrementos de 0.25 en el eje Y
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()

# Lista de señales y títulos
senales = [senoidal, cuadrada, triangular, diente_de_sierra]
titulos = ['Senoidal', 'Cuadrada', 'Triangular', 'Diente de Sierra']

# Graficar cada señal una por una
for senal, titulo in zip(senales, titulos):
    graficar_senales(tiempo, senal, titulo)
