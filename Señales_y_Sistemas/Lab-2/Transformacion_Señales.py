import numpy as np
import matplotlib.pyplot as plt

desp = -5  # Desplazamiento a la derecha
factor = 0.5  # Contracción
# Parámetros iniciales y señales aperiódicas
tiempo = np.linspace(-5, 15, 1000, endpoint=False)  # Tiempo de 0 a 5 segundos
impulso = np.zeros_like(tiempo)
impulso[0] = 1
exp_decreciente = np.exp(-tiempo) * (tiempo >= 0) * (tiempo <= 1)
exp_creciente = np.exp(tiempo) * (tiempo >= 0) * (tiempo <= 1)
escalon = np.heaviside(tiempo, 1)
sinc = np.sinc(tiempo / np.pi)
# Parámetros de desplazamiento y contracción


# Función para desplazar y contraer la señal
def transformar_senal(t, senal, desp, factor):
    t_transformado = (t - desp) * factor
    return t_transformado, senal

# Graficar señales transformadas
def graficar_senales(t, senal, titulo):
    plt.figure(figsize=(10, 6))
    plt.plot(t, senal)
    plt.title(titulo)
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()

# Transformar y graficar cada señal aperiódica
for senal, titulo in zip([impulso, exp_decreciente, exp_creciente, escalon, sinc], 
                         ['Impulso', 'Exponencial Decreciente', 'Exponencial Creciente', 'Escalón', 'Sinc']):
    t_transformado, senal_transformada = transformar_senal(tiempo, senal, desp, factor)
    graficar_senales(t_transformado, senal_transformada, f"{titulo} - Transformada (Desplazamiento y Contracción)")
