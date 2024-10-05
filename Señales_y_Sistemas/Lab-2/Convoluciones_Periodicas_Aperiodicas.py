import numpy as np
import matplotlib.pyplot as plt

# Parámetros iniciales para señales aperiódicas
tiempo_ap = np.linspace(0, 5, 1000, endpoint=False)  # Tiempo de 0 a 5 segundos

# Señales aperiódicas
# Exponencial decreciente
exp_decreciente = np.exp(-tiempo_ap) * (tiempo_ap >= 0) * (tiempo_ap <= 1)

# Exponencial creciente
exp_creciente = np.exp(tiempo_ap) * (tiempo_ap >= 0) * (tiempo_ap <= 1)

# Impulso
impulso = np.zeros_like(tiempo_ap)
impulso[0] = 1  # Definimos el impulso en t=0

# Escalón
escalon = np.heaviside(tiempo_ap, 1)  # Heaviside es la función escalón

# Sinc
sinc = np.sinc(tiempo_ap / np.pi)  # np.sinc normalizado

# Parámetros iniciales para señales periódicas
tiempo_per = np.linspace(0, 5, 1000, endpoint=False)  # Tiempo de 0 a 5 segundos
frecuencia = 2 * np.pi  # Frecuencia angular de 2*pi
desfase = np.pi / 4     # Desfase de pi/4 radianes

# Señales periódicas
senoidal = np.sin(frecuencia * tiempo_per + desfase)
cuadrada = np.sign(np.sin(frecuencia * tiempo_per + desfase))
triangular = np.abs((frecuencia * tiempo_per + desfase) % 4 - 2) - 1
diente_de_sierra = (frecuencia * tiempo_per + desfase) % 2 - 1

# Función para graficar señales individualmente con ajuste de ejes
def graficar_senales(t, senal, titulo):
    plt.figure(figsize=(10, 6))  # Aumentar el alto del gráfico
    plt.plot(t, senal)
    plt.title(titulo)
    plt.xlim(0, 5)  # Rango de 0 a 5 en el eje X
    plt.ylim(-1.5, 1.5)  # Rango ajustado en el eje Y
    plt.xticks(np.arange(0, 6, 1))  # Incrementos de 1 en el eje X
    plt.yticks(np.arange(-1.5, 2, 0.5))  # Incrementos de 0.5 en el eje Y
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()

# Función para convolucionar señales y graficar resultados
def convolucionar_y_graficar(senal_periodica, senal_aperiodica, titulo):
    # Realizar la convolución
    convolucion = np.convolve(senal_periodica, senal_aperiodica, mode='full')
    # Crear un nuevo tiempo para la señal convolucionada
    tiempo_conv = np.linspace(0, len(convolucion) / 1000, len(convolucion), endpoint=False)
    
    # Graficar la señal convolucionada
    plt.figure(figsize=(10, 6))
    plt.plot(tiempo_conv, convolucion)
    plt.title(f'Convolución de {titulo}')
    plt.xlim(0, 5)  # Ajustar el rango de tiempo en el eje X
    plt.ylim(-2, 2)  # Ajustar el rango del eje Y
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()

# Lista de señales periódicas y sus títulos
senales_periodicas = [senoidal, cuadrada, triangular, diente_de_sierra]
titulos_periodicos = ['Senoidal', 'Cuadrada', 'Triangular', 'Diente de Sierra']

# Lista de señales aperiódicas
senales_aperiodicas = [exp_decreciente, exp_creciente, impulso, escalon, sinc]
titulos_aperiodicos = ['Exponencial Decreciente', 'Exponencial Creciente', 'Impulso', 'Escalón', 'Sinc']

# Convolucionar cada señal periódica con una señal aperiódica
for senal_per, titulo_per in zip(senales_periodicas, titulos_periodicos):
    for senal_ap, titulo_ap in zip(senales_aperiodicas, titulos_aperiodicos):
        convolucionar_y_graficar(senal_per, senal_ap, f'{titulo_per} con {titulo_ap}')
