# README - Simulación de Paginación

## Introducción

Este documento describe la implementación final de la simulación de paginación, incluyendo la asignación de memoria física y virtual, la creación y finalización de procesos, el manejo de page faults y la política de reemplazo de páginas (FIFO). Además, se detalla cómo esta implementación cumple con los criterios de la rúbrica anteriormente entregada.

La simulación crea procesos periódicamente, finaliza procesos al azar, accede a direcciones virtuales para provocar page faults, y gestiona las páginas entre RAM y Swap. Al agotarse la memoria (RAM + Swap), el programa finaliza mostrando un mensaje descriptivo.

## Instrucciones de Compilación y Ejecución

1. **Compilación:**
   ```bash
   gcc main.c -o simulacion -pthread

2. **Ejecucion:**
   ```bash
   ./simulacion

3. **Interacción con el Programa:**
   - Al ejecutar el programa, se solicitará el tamaño de la memoria física (en MB) y el tamaño de las páginas (en KB).
      - Puedes ingresar, por ejemplo, 64 MB para la memoria física.
      - Para el tamaño de páginas, un valor típico puede ser 4 KB.
   
      - Estos valores se pueden ajustar según las necesidades de la simulación. La memoria virtual se calculará automáticamente entre 1.5 y 4.5 veces la memoria física.

   - Una vez ingresados, iniciará la creación de procesos, el acceso a direcciones virtuales y la finalización de procesos.
   
   - En pantalla se mostrarán mensajes indicando creación de procesos, accesos virtuales, page faults, reemplazo de páginas y finalización de procesos.
   
   

## Cumplimiento de la Rúbrica

A continuación se detalla cómo esta implementación cumple con cada ítem de la rúbrica:

1. **Parámetros de memoria y páginas:**  
   - Solicita memoria física (MB) y tamaño de página (KB).
   - Calcula memoria virtual (1.5 a 4.5 veces la física).
   - Muestra resultados y valida entradas.
   - Se crean nuevos procesos cada 2 segundos desde el inicio.

2. **Page faults y política de reemplazo:**  
   - Genera page faults cuando la página solicitada no está en RAM.
   - Aplica política FIFO para reemplazar páginas en RAM por páginas en Swap.

3. **Acceso a direcciones virtuales (cada 5 segundos después de 30 segundos):**  
   - A partir de los 30 segundos de ejecución, cada 5 segundos se accede aleatoriamente a una dirección virtual.
   - Esto permite observar page faults cuando corresponda.

4. **Finalización de procesos (cada 5 segundos después de 30 segundos):**  
   - Durante los primeros 30 segundos, solo se crean procesos cada 2 segundos.
   - Tras 30 segundos de ejecución, se inicia la finalización de un proceso aleatorio cada 5 segundos, liberando sus páginas de RAM y Swap.

5. **Mensaje al agotar memoria:**  
   - Si no hay más marcos en RAM ni en Swap, el programa muestra un mensaje descriptivo y finaliza ordenadamente.

6. **Creación/Finalización simulada adecuadamente:**  
   - Procesos de distintos tamaños se crean cada 2 segundos.
   - Después de 30 segundos, además de acceder a direcciones virtuales cada 5 segundos, se finaliza un proceso aleatorio cada 5 segundos.
   - Esta dinámica asegura la simulación correcta de creación, acceso y finalización.

## Estructura del Código y Funciones Principales

La implementación se basa en varios componentes clave:

- **Estructuras de datos:**
  - `Proceso`: Representa cada proceso con un ID, tamaño y una tabla de páginas.
  - `Pagina`: Representa las páginas de cada proceso, indicando si están en RAM o en Swap.
  - Memoria representada con vectores: uno para RAM y otro para Swap.

- **Funciones principales:**
  - `inicializar_sistema()`: Solicita y valida parámetros de memoria, calcula memoria virtual y marcos.
  - `crear_proceso()`: Crea procesos de tamaño aleatorio, asignando sus páginas a RAM o Swap.
  - `finalizar_proceso()`: Selecciona un proceso aleatorio y libera sus páginas (RAM y Swap).
  - `acceder_direccion_virtual()`: Accede a una dirección virtual aleatoria; si la página no está en RAM, genera un page fault y aplica el reemplazo FIFO.
  - `manejar_page_fault()`: Realiza el reemplazo de páginas cuando la RAM está llena, moviendo páginas a Swap.

- **Hilos (Threads):**
  - Un hilo para crear procesos periódicamente.
  - Un hilo para finalizar procesos cada cierto intervalo.
  - Un hilo para acceder a direcciones virtuales y generar page faults.

Estos hilos se ejecutan en paralelo, utilizando mutex para evitar condiciones de carrera al acceder a estructuras compartidas.

## Consideraciones Adicionales

- **Sincronización:**  
  Uso de mutex para evitar condiciones de carrera al acceder a RAM, Swap y lista de procesos.

- **Adaptabilidad:**  
  Parámetros ajustables (tamaño de procesos, frecuencia de creación/finalización, intervalos).

- **Extensibilidad:**  
  Fácil de implementar otras políticas de reemplazo de páginas (LRU, LFU, etc.) si se desea.



