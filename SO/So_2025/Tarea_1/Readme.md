Simulador de Planificación de CPU - FCFS

Este proyecto simula una planificación de tareas por CPU utilizando el algoritmo First Come First Serve (FCFS). Está compuesto por un proceso central que se comunica con múltiples procesos independientes a través de pipes nombrados (FIFOs).

1. Objetivo

Simular un entorno en el que procesos independientes (entre 2 y 6) generan tareas aleatorias que deben ser ejecutadas por una CPU simulada en un proceso central. Cada tarea posee un identificador, tiempo de llegada y tiempo de ejecución (burst). El proceso central ejecuta todas las tareas en orden de llegada y despliega información relevante al término de cada una.

2. Estructura del Proyecto

Central.c: Proceso central que lanza los procesos independientes, recolecta tareas y las ejecuta.

Proceso.c: Proceso que genera entre 3 y 6 tareas con datos aleatorios y las envía al proceso central.

3. Comunicación entre procesos

Se utilizan pipes nombrados para la comunicación entre los procesos independientes y el central:

Cada proceso independiente escribe sus tareas en un pipe /tmp/pipe_procesoX, donde X es su ID (de 0 a N-1).

El proceso central lee desde cada pipe, almacena las tareas y las ejecuta ordenadas por tiempo de llegada.

4. Algoritmo de Planificación

Se implementa el algoritmo First Come First Serve (FCFS):

Las tareas se ejecutan en el orden de su tiempo de llegada.

Si una tarea llega más tarde que el tiempo actual, se espera hasta su llegada.

Se calcula y muestra el Turnaround (tiempo de finalización - tiempo de llegada).

5. Compilación

$ gcc -o Central Central.c
$ gcc -o Proceso Proceso.c

6. Ejecución

$ ./Central N

Donde N es el número de procesos independientes (entre 2 y 6). El proceso central creará los pipes, lanzará los procesos con fork() y exec() y recibirá sus tareas.

7. Ejemplo de Salida

[PID 49558] ID: 0 | Llegada: 1 | Fin: 3 | Turnaround: 2
[PID 49626] ID: 1 | Llegada: 4 | Fin: 7 | Turnaround: 3
...

8. Paso a paso del código

Central.c

Lectura de argumento N: cantidad de procesos independientes.

Creación de pipes nombrados: uno por cada proceso.

Creación de procesos: se lanza N veces Proceso con exec.

Lectura de tareas: el central lee tareas de cada pipe y las almacena.

Ordenamiento: las tareas se ordenan según tiempo de llegada.

Ejecución FCFS: se simula la ejecución, mostrando PID, ID, llegada, fin y turnaround.

Proceso.c

Lectura del argumento de ID: cada proceso recibe su número.

Generación aleatoria: se crean entre 3 y 6 tareas con tiempos aleatorios.

Envío de tareas: cada tarea se escribe al pipe correspondiente.

Finalización: luego de enviar todas las tareas, el proceso termina.

9. Restricciones

No se permiten threads, mutexes ni semáforos.

Solo se usan procesos y pipes nombrados.

Las tareas deben generarse de forma aleatoria en tiempo de llegada y burst.



