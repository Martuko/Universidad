import numpy as np
import matplotlib.pyplot as plt

# Parámetros de transformación
desplazamiento = -5  # Desplazamiento hacia la derecha
factor = 2  # Factor de contracción

# Rango de tiempo de 0 a 15 segundos
tiempo = np.linspace(0, 15, 1000)  # Tiempo de 0 a 15 segundos

# Creación de señales aperiódicas originales
# Exponencial decreciente
exp_decreciente = np.exp(-(tiempo)) * (tiempo >= 0) * (tiempo <= 1)
# Exponencial creciente
exp_creciente = np.exp(tiempo) * (tiempo >= 0) * (tiempo <= 1)

# Impulso
impulso = np.zeros_like(tiempo)
impulso[0] = 1  # Definimos el impulso en t=0

# Escalón
escalon = np.heaviside(tiempo, 1)  # Heaviside es la función escalón

# Sinc
sinc = np.sinc(tiempo / np.pi)  # np.sinc normalizado

# Aplicar las transformaciones: desplazamiento y contracción
tiempo_transformado = (tiempo - desplazamiento) / factor

# Recalcular las señales después de aplicar las transformaciones
# Exponencial decreciente transformada
exp_decreciente_transformada = np.exp(-(tiempo_transformado)) * (tiempo_transformado >= 0)
# Exponencial creciente transformada
exp_creciente_transformada = np.exp(tiempo_transformado) * (tiempo_transformado >= 0)
# Impulso transformado
impulso_transformado = np.zeros_like(tiempo_transformado)
impulso_transformado[0] = 1  # Se mantiene el valor del impulso en t=0
# Escalón transformado
escalon_transformado = np.heaviside(tiempo_transformado, 1)  # Heaviside es la función escalón transformada
# Sinc transformado
sinc_transformado = np.sinc(tiempo_transformado / np.pi)  # np.sinc normalizado transformada

# Función para graficar señales
def graficar_senales(tiempo, senal_original, senal_transformada, nombre):
    plt.figure(figsize=(10, 6))
    
    # Graficar la señal original
    plt.subplot(2, 1, 1)
    plt.plot(tiempo, senal_original, label='Original', color='blue')
    plt.title(f'Señal Original: {nombre}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel(nombre)
    plt.grid(True)
    plt.legend()

    # Graficar la señal transformada
    plt.subplot(2, 1, 2)
    plt.plot(tiempo_transformado, senal_transformada, label='Transformada', color='red')
    plt.title(f'Señal Transformada: {nombre}')
    plt.xlabel('Tiempo Transformado (s)')
    plt.ylabel(nombre)
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.show()

# Graficar las señales originales y transformadas
graficar_senales(tiempo, exp_decreciente, exp_decreciente_transformada, 'Exponencial Decreciente')
graficar_senales(tiempo, exp_creciente, exp_creciente_transformada, 'Exponencial Creciente')
graficar_senales(tiempo, impulso, impulso_transformado, 'Impulso')
graficar_senales(tiempo, escalon, escalon_transformado, 'Escalón')
graficar_senales(tiempo, sinc, sinc_transformado, 'Sinc')
