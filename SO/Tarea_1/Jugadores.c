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

void jugador(int id, int num_jugadores, int jugador_eliminado);

int main() {
    int num_jugadores;

    printf("Ingrese el número de jugadores: ");
    scanf("%d", &num_jugadores);

    if (num_jugadores < 2) {
        printf("El número de jugadores debe ser al menos 2.\n");
        exit(EXIT_FAILURE);
    }

    mkfifo(PIPE_NAME, 0666);
    mkfifo(RESULT_PIPE, 0666);

    pid_t pid;

    // Crear proceso observador
    pid = fork();
    if (pid == 0) {
        execl("./observador", "observador", NULL); // Ejecutar el código del observador
        exit(0);
    } else if (pid < 0) {
        perror("Error creando el proceso observador");
        exit(EXIT_FAILURE);
    }

    int i;
    for (i = 0; i < num_jugadores; i++) {
        pid = fork();
        if (pid == 0) {
            jugador(i + 1, num_jugadores, -1); // Cada jugador se crea con su ID
            exit(0);
        } else if (pid < 0) {
            perror("Error creando el proceso jugador");
            exit(EXIT_FAILURE);
        }
    }

    // Esperar a que todos los procesos (jugadores y observador) terminen
    for (i = 0; i < num_jugadores + 1; i++) {
        wait(NULL);
    }

    // Leer el jugador eliminado desde el pipe de resultados
    int jugador_eliminado;
    int result_pipe_fd = open(RESULT_PIPE, O_RDONLY);
    read(result_pipe_fd, &jugador_eliminado, sizeof(int));
    close(result_pipe_fd);

    // Reiniciar los jugadores para que verifiquen si son eliminados
    for (i = 0; i < num_jugadores; i++) {
        pid = fork();
        if (pid == 0) {
            jugador(i + 1, num_jugadores, jugador_eliminado); // Reenviar con el jugador eliminado
            exit(0);
        } else if (pid < 0) {
            perror("Error creando el proceso jugador");
            exit(EXIT_FAILURE);
        }
    }

    // Esperar a que todos los procesos terminen
    for (i = 0; i < num_jugadores; i++) {
        wait(NULL);
    }

    printf("Jugador %d fue eliminado.\n", jugador_eliminado);
    unlink(PIPE_NAME);
    unlink(RESULT_PIPE);
    return 0;
}

void jugador(int id, int num_jugadores, int jugador_eliminado) {
    // Verificar si el jugador es el eliminado
    if (id == jugador_eliminado) {
        execl("./amurrado", "amurrado", NULL); // Llamar al código de amurrado si el jugador está eliminado
        exit(0);
    }

    printf("Jugador %d está listo.\n", id);
    sleep(1);

    int pipe_fd = open(PIPE_NAME, O_WRONLY);
    if (pipe_fd == -1) {
        perror("Error abriendo el pipe");
        exit(EXIT_FAILURE);
    }

    srand(time(NULL) + id);
    int voto = (rand() % num_jugadores) + 1;
    printf("Jugador %d vota por el jugador %d\n", id, voto);

    char voto_str[10];
    sprintf(voto_str, "%d", voto);
    write(pipe_fd, voto_str, strlen(voto_str) + 1);
    close(pipe_fd);
}
