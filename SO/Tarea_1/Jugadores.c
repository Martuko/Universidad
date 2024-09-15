#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <sys/wait.h>

#define PIPE_NAME "votos_pipe"
#define RESULT_PIPE "resultado_pipe"

int num_jugadores = 10;
int sincronizacion_pipes[10][2]; // Pipes para iniciar votación a cada jugador
int confirmacion_pipes[10][2];   // Pipes para confirmar votación/eliminación
pid_t jugadores_pids[10];

void crear_jugadores();
void votar();
void eliminar_jugador(int jugador_eliminado);
void jugador(int id);
void iniciar_votacion(int id);
void recrear_pipes();
void verificar_pipes();

int main() {
    recrear_pipes();

    printf("Ejecuta el Observador en otra terminal antes de continuar.\n");

    crear_jugadores();

    // Bucle principal del juego
    while (num_jugadores > 1) {
        printf("Todos los jugadores están listos. Iniciando la votación.\n");

        votar();

        int jugador_eliminado;
        int result_pipe_fd = open(RESULT_PIPE, O_RDONLY);
        if (result_pipe_fd == -1) {
            perror("Error abriendo el pipe de resultados");
            exit(EXIT_FAILURE);
        }
        // Lee el jugador eliminado del pipe de resultados
        read(result_pipe_fd, &jugador_eliminado, sizeof(int));
        close(result_pipe_fd);

        eliminar_jugador(jugador_eliminado);

        // Imprimir el número de jugadores restantes
        printf("Número de jugadores restantes: %d\n", num_jugadores);

        // Recrear los pipes para la siguiente ronda
        recrear_pipes();
        verificar_pipes();
        sleep(1);  // Espera breve para asegurar sincronización
    }

    printf("¡El jugador final es el ganador!\n");
    unlink(PIPE_NAME);
    unlink(RESULT_PIPE);

    return 0;
}

void crear_jugadores() {
    for (int i = 0; i < num_jugadores; i++) {
        // Crear pipes para sincronizar votación y confirmar acciones de cada jugador
        if (pipe(sincronizacion_pipes[i]) == -1 || pipe(confirmacion_pipes[i]) == -1) {
            perror("Error creando pipes de sincronización");
            exit(EXIT_FAILURE);
        }

        jugadores_pids[i] = fork();
        if (jugadores_pids[i] == 0) {
            close(sincronizacion_pipes[i][1]); // Cerrar la escritura del pipe de sincronización en el hijo
            close(confirmacion_pipes[i][0]);   // Cerrar la lectura del pipe de confirmación en el hijo
            jugador(i + 1);
            exit(0);
        }
        close(sincronizacion_pipes[i][0]); // Cerrar la lectura del pipe de sincronización en el padre
        close(confirmacion_pipes[i][1]);   // Cerrar la escritura del pipe de confirmación en el padre
    }
}

void votar() {
    printf("Enviando mensajes de votación a cada jugador...\n");
    char mensaje[] = "VOTAR";

    for (int i = 0; i < num_jugadores; i++) {
        printf("Enviando mensaje de votación al jugador con PID %d.\n", jugadores_pids[i]);
        write(sincronizacion_pipes[i][1], mensaje, sizeof(mensaje)); // Enviar la instrucción de votar

        // Esperar confirmación de que el jugador ha completado su votación
        char confirmacion[10];
        read(confirmacion_pipes[i][0], confirmacion, sizeof(confirmacion));
        printf("Jugador con PID %d ha completado su votación.\n", jugadores_pids[i]);
    }
}

void eliminar_jugador(int jugador_eliminado) {
    int index = jugador_eliminado - 1;
    if (index >= 0 && index < num_jugadores) {
        printf("Eliminando jugador %d con PID %d.\n", jugador_eliminado, jugadores_pids[index]);

        // Enviar un mensaje de eliminación al jugador
        char mensaje[] = "ELIMINAR";
        write(sincronizacion_pipes[index][1], mensaje, sizeof(mensaje));

        // Esperar confirmación de que el jugador ha sido eliminado
        char confirmacion[10];
        read(confirmacion_pipes[index][0], confirmacion, sizeof(confirmacion));

        // Ajustar el array de PIDs y pipes para eliminar al jugador
        for (int i = index; i < num_jugadores - 1; i++) {
            jugadores_pids[i] = jugadores_pids[i + 1];
            sincronizacion_pipes[i][0] = sincronizacion_pipes[i + 1][0];
            sincronizacion_pipes[i][1] = sincronizacion_pipes[i + 1][1];
            confirmacion_pipes[i][0] = confirmacion_pipes[i + 1][0];
            confirmacion_pipes[i][1] = confirmacion_pipes[i + 1][1];
        }
        num_jugadores--;
    } else {
        printf("Índice de jugador eliminado fuera de rango.\n");
    }
}

void jugador(int id) {
    printf("Jugador %d está listo.\n", id);

    while (1) {
        // Leer desde el pipe de sincronización para saber si debe votar o ser eliminado
        char buffer[10];
        read(sincronizacion_pipes[id - 1][0], buffer, sizeof(buffer));

        if (strcmp(buffer, "VOTAR") == 0) {
            iniciar_votacion(id);
        } else if (strcmp(buffer, "ELIMINAR") == 0) {
            printf("Jugador %d (PID %d) está siendo eliminado.\n", id, getpid());
            write(confirmacion_pipes[id - 1][1], "OK", 3); // Confirmar eliminación
            exit(0); // El jugador se retira
        }
    }
}

void iniciar_votacion(int id) {
    printf("Jugador con PID %d está votando...\n", getpid());

    int pipe_fd = open(PIPE_NAME, O_WRONLY);
    if (pipe_fd == -1) {
        perror("Error abriendo el pipe de votos");
        exit(EXIT_FAILURE);
    }

    srand(time(NULL) + getpid());
    int voto = (rand() % num_jugadores) + 1;
    printf("Jugador con PID %d votó por el jugador %d.\n", getpid(), voto);

    write(pipe_fd, &voto, sizeof(voto));
    close(pipe_fd);

    // Confirmar al proceso principal que ha terminado de votar
    write(confirmacion_pipes[id - 1][1], "OK", 3);
}

void recrear_pipes() {
    // Elimina los pipes si existen
    unlink(PIPE_NAME);
    unlink(RESULT_PIPE);

    // Crea los pipes nuevamente
    if (mkfifo(PIPE_NAME, 0666) == -1) {
        perror("Error creando PIPE_NAME");
        exit(EXIT_FAILURE);
    }
    if (mkfifo(RESULT_PIPE, 0666) == -1) {
        perror("Error creando RESULT_PIPE");
        exit(EXIT_FAILURE);
    }
}

void verificar_pipes() {
    char buffer[100];
    int fd = open(PIPE_NAME, O_RDONLY | O_NONBLOCK);
    if (fd != -1) {
        if (read(fd, buffer, sizeof(buffer)) > 0) {
            printf("Contenido inesperado en %s: %.*s\n", PIPE_NAME, (int) sizeof(buffer), buffer);
        } else {
            printf("PIPE_NAME está limpio para la siguiente ronda.\n");
        }
        close(fd);
    }

    fd = open(RESULT_PIPE, O_RDONLY | O_NONBLOCK);
    if (fd != -1) {
        if (read(fd, buffer, sizeof(buffer)) > 0) {
            printf("Contenido inesperado en %s: %.*s\n", RESULT_PIPE, (int) sizeof(buffer), buffer);
        } else {
            printf("RESULT_PIPE está limpio para la siguiente ronda.\n");
        }
        close(fd);
    }
}
