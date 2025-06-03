# DAG Path Finder

Este proyecto contiene dos implementaciones en C++ para encontrar rutas de costo mínimo en un grafo acíclico dirigido (DAG), utilizando múltiples hilos (`threads`) para realizar búsquedas aleatorias de rutas. 

Los códigos disponibles son:

- `SinLimite.cpp`: Búsqueda concurrente sin restricciones de uso de aristas.
- `ConLimite.cpp`: Búsqueda concurrente con un límite máximo de uso por arista (simulación de contención de recursos compartidos).

## Descripción general

Ambos programas generan un DAG de 62 nodos distribuidos en 14 niveles. Se busca encontrar rutas desde el nodo inicial (0) al final (61), minimizando el costo acumulado al recorrer las aristas. Cada ejecución utiliza múltiples hilos que exploran rutas aleatorias durante 60 segundos. Se registra el mejor costo encontrado y se guarda en archivos `.csv`.

### Características:
- Uso de `threads` y `mutex` para concurrencia segura.
- Exportación de resultados en archivos:
  - `actual.csv`: Ruta más barata encontrada.
  - `costos.csv`: Historial del mejor costo en el tiempo.
- En `ConLimite.cpp`, se simula una contención real limitando cuántos hilos pueden usar simultáneamente una misma arista.

---

## ¿Cómo compilar?

Usa `g++` con soporte para C++11 o superior. En consola:

### Para `SinLimite.cpp`:
```bash
g++ -std=c++11 -pthread SinLimite.cpp -o SinLimite
```
### Para `Conimite.cpp`:
```bash
g++ -std=c++17 -pthread ConLimite.cpp -o ConLimite
```

## ¿Cómo ejecutar?

### Para `SinLimite.cpp`:
```bash
./SinLimite
```
### Para `Conimite.cpp`:
```bash
./ConLimite
```
- Se te solicitara:
 - La cantidad de threads
 - El limite de threads por arista

## Ejemplo de salida esperada:

```bash
Ingrese el número de threads a usar (1, 10, 20, 50, 100): 50
Nuevo mejor costo encontrado: 152
Nuevo mejor costo encontrado: 147
...
== Mejor ruta encontrada (Costo: 135) ==
0 5 12 19 26 33 40 47 54 55 56 57 58 59 61
```

## Archivos generados
- Al finalizar la ejecución, se generan:
 - actual.csv: la mejor ruta encontrada durante los 60 segundos.
 - costos.csv: pares (tiempo, costo) indicando cuándo se mejoró el mejor costo.
- Puedes abrir estos archivos con Excel o cualquier visor de texto para análisis posterior.

## Requisitos
- CompiladorCompilador g++ con soporte para C++11 o superior.
- Sistema operativo con soporte para hilos POSIX (Linux, Mac, WSL, etc.).



