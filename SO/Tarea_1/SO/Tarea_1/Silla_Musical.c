#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <time.h>
#include <sys/wait.h>

#define PIPE_NAME "votos_pipe" // Nombre del pipe para la comunicación

// Declaración de funciones
void jugador(int id, int num_jugadores);
void observador(int num_jugadores);
void eliminar_pipe(); // Función para eliminar el pipe
pid_t main_pid;       // Variable global para almacenar el PID del proceso principal

int main() {
    int num_jugadores;

    // Solicitar al usuario el número de jugadores
    printf("Ingrese el número de jugadores: ");
    scanf("%d", &num_jugadores);

    // Validar que el número de jugadores sea mayor que 1
    if (num_jugadores < 2) {
        printf("El número de jugadores debe ser al menos 2.\n");
        exit(EXIT_FAILURE);
    }

    main_pid = getpid(); // Guardar el PID del proceso principal
    atexit(eliminar_pipe); // Registrar la eliminación del pipe cuando el programa termine

    while (num_jugadores > 1) {
        // Crear pipe con nombre para la comunicación de los votos
        if (mkfifo(PIPE_NAME, 0666) == -1) {
            perror("Error creando el pipe");
            exit(EXIT_FAILURE);
        }

        pid_t pid;
        int i;

        // Crear proceso observador
        pid = fork();
        if (pid == 0) {
            observador(num_jugadores); // Observador maneja el número de jugadores
            exit(0);
        } else if (pid < 0) {
            perror("Error creando el proceso observador");
            exit(EXIT_FAILURE);
        }

        // Crear procesos jugadores
        for (i = 0; i < num_jugadores; i++) {
            pid = fork();
            if (pid == 0) {
                jugador(i + 1, num_jugadores); // Cada jugador tiene un ID único
                exit(0);
            } else if (pid < 0) {
                perror("Error creando el proceso jugador");
                exit(EXIT_FAILURE);
            }
        }

        // Esperar a que todos los procesos terminen
        for (i = 0; i < num_jugadores + 1; i++) { // +1 por el observador
            wait(NULL);
        }

        // Reducir el número de jugadores en 1
        num_jugadores--;

        // Eliminar el pipe al final de la ronda
        unlink(PIPE_NAME);
    }

    printf("Juego terminado. ¡Solo queda un jugador!\n");
    return 0;
}

void eliminar_pipe() {
    // Solo el proceso principal elimina el pipe
    if (getpid() == main_pid) {
        if (unlink(PIPE_NAME) == -1) {
            perror("Error eliminando el pipe");
        } else {
            printf("Pipe eliminado correctamente.\n");
        }
    }
}

void jugador(int id, int num_jugadores) {
    // Simulación de un jugador con identificador 'id'
    printf("Jugador %d está listo.\n", id);
    sleep(1); // Espera para sincronizar a todos los jugadores

    // Abrir el pipe para enviar el voto al observador
    int pipe_fd = open(PIPE_NAME, O_WRONLY);
    if (pipe_fd == -1) {
        perror("Error abriendo el pipe");
        exit(EXIT_FAILURE);
    }

    // Generar un voto aleatorio (votar por otro jugador)
    srand(time(NULL) + id); // Semilla aleatoria basada en el ID del jugador
    int voto = (rand() % num_jugadores) + 1; // Genera un voto entre 1 y el número total de jugadores
    printf("Jugador %d vota por el jugador %d\n", id, voto);

    // Enviar el voto al observador
    char voto_str[10];
    sprintf(voto_str, "%d", voto);
    write(pipe_fd, voto_str, strlen(voto_str) + 1);
    close(pipe_fd);
}

void observador(int num_jugadores) {
    // Lógica del observador que recibe los votos y determina quién es eliminado
    printf("Observador está listo.\n");
    sleep(2); // Espera para asegurarse de que todos los jugadores hayan votado

    // Abrir el pipe para leer los votos
    int pipe_fd = open(PIPE_NAME, O_RDONLY);
    if (pipe_fd == -1) {
        perror("Error abriendo el pipe");
        exit(EXIT_FAILURE);
    }

    // Crear un arreglo dinámico para contar los votos, ajustado al número de jugadores
    int *votos = (int *)calloc(num_jugadores + 1, sizeof(int));
    if (votos == NULL) {
        perror("Error al asignar memoria para los votos");
        exit(EXIT_FAILURE);
    }

    // Leer los votos y contabilizarlos
    char buffer[10];
    for (int i = 0; i < num_jugadores; i++) {
        if (read(pipe_fd, buffer, sizeof(buffer)) > 0) {
            int voto = atoi(buffer);
            if (voto >= 1 && voto <= num_jugadores) {
                votos[voto]++;
            }
        }
    }
    close(pipe_fd);

    // Determinar quién fue el más votado
    int max_votos = 0;
    int jugador_eliminado = -1;
    for (int i = 1; i <= num_jugadores; i++) {
        if (votos[i] > max_votos) {
            max_votos = votos[i];
            jugador_eliminado = i;
        }
    }

    // En caso de empate, elegir uno al azar (no implementado completamente)
    printf("Jugador %d fue el más votado y debe abandonar el juego.\n", jugador_eliminado);
    free(votos); // Liberar la memoria asignada para los votos
}