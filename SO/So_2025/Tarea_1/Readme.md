
# Simulador de Planificación FCFS con Pipes en C

Este proyecto simula la planificación de procesos bajo el algoritmo **First Come First Served (FCFS)**. Se implementa mediante múltiples procesos que generan tareas y las envían a un proceso central usando **named pipes (FIFOs)** para su posterior planificación.

## Archivos

- `central.c`: proceso central que recibe tareas desde procesos externos y las ejecuta usando FCFS.
- `proceso.c`: procesos secundarios que generan tareas aleatorias y las envían al proceso central mediante pipes.

---

## ¿Cómo funciona?

### 1. `proceso.c` (Procesos generadores)

- Recibe como argumento un ID (de 0 a 5).
- Abre un FIFO específico `/tmp/pipe_proceso<ID>`.
- Genera entre 3 y 6 tareas aleatorias con:
  - `arrival`: tiempo de llegada (0–9)
  - `burst`: duración de la tarea (1–5)
- Cada tarea se envía al FIFO, incluyendo el `PID` del proceso.

### 2. `central.c` (Proceso principal)

- Recibe como argumento la cantidad de procesos a leer (2 a 6).
- Crea los FIFOs necesarios `/tmp/pipe_proceso<ID>`.
- Lee todas las tareas de cada FIFO.
- Ordena las tareas por tiempo de llegada (`arrival`) usando el algoritmo FCFS.
- Muestra:
  - PID del proceso que envió la tarea
  - ID de la tarea
  - Tiempo de llegada
  - Tiempo de finalización
  - Turnaround time

---

## Ejecución paso a paso

### 1. Compilar

```bash
gcc central.c -o central
gcc proceso.c -o proceso
```

### 2. Ejecutar los procesos generadores

En terminales separadas:

```bash
./proceso 0
./proceso 1
...
./proceso N
```

> Puedes ejecutar entre 2 y 6 procesos con IDs del 0 al 5.

### 3. Ejecutar el proceso central

Después de que los procesos hayan enviado las tareas:

```bash
./central N
```

Donde `N` es el número de procesos usados.

---

## Ejemplo de salida

```
[PID 1243] ID: 0 | Llegada: 2 | Fin: 6 | Turnaround: 4
[PID 1251] ID: 1 | Llegada: 3 | Fin: 10 | Turnaround: 7
...
```

---

## Limpieza

Borra los pipes con:

```bash
rm /tmp/pipe_proceso*
```

---

s.
