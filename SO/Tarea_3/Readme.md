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
   -El programa solicitará el tamaño de la memoria física (en MB) y el tamaño de las páginas (en KB).
   
   -Una vez ingresados, iniciará la creación de procesos, el acceso a direcciones virtuales y la finalización de procesos.
   
   -En pantalla se mostrarán mensajes indicando creación de procesos, accesos virtuales, page faults, reemplazo de páginas y finalización de procesos.
   
   -Presione Enter cuando desee terminar la simulación.

## Cumplimiento de la Rúbrica

A continuación se detalla cómo esta implementación cumple con cada ítem de la rúbrica:

1. **Parámetros de memoria y páginas:**  
   - Solicita memoria física (MB) y tamaño de página (KB).
     
   - Calcula memoria virtual (1.5 a 4.5 veces la física).
     
   - Muestra resultados y valida entradas.

2. **Page faults y política de reemplazo:**  
   - Genera page faults cuando la página solicitada no está en RAM.
     
   - Aplica política FIFO para reemplazar páginas en RAM por páginas en Swap.

3. **Acceso a direcciones virtuales (cada 5 segundos):**  
   - Accede aleatoriamente a direcciones virtuales.
   - Muestra page faults cuando corresponda.

4. **Finalización de procesos (cada 5 segundos):**  
   - Finaliza un proceso aleatorio, liberando sus páginas de RAM y Swap.

5. **Mensaje al agotar memoria:**  
   - Si no hay más marcos en RAM ni en Swap, el programa muestra un mensaje y finaliza.

6. **Creación/Finalización simulada adecuadamente:**  
   - Procesos de distintos tamaños, asignación de páginas a RAM/Swap según disponibilidad.

7. **Compilación y legibilidad:**  
   - Código claro, con comentarios y uso de librerías estándar.
   - Fácil de seguir en tiempo de ejecución.

## Consideraciones Adicionales

- **Sincronización:**  
  Uso de mutex para evitar condiciones de carrera al acceder a RAM, Swap y lista de procesos.

- **Adaptabilidad:**  
  Parámetros ajustables (tamaño de procesos, frecuencia de creación/finalización, intervalos).

- **Extensibilidad:**  
  Fácil de implementar otras políticas de reemplazo de páginas (LRU, LFU, etc.) si se desea.

## Conclusión

La implementación cumple con las especificaciones, simula el mecanismo de paginación con asignación de páginas a RAM y Swap, genera page faults, finaliza procesos, y muestra mensajes descriptivos. Este README provee información para compilar, ejecutar y entender el funcionamiento, así como la relación con la rúbrica.

