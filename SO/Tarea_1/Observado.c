
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>

#define PIPE_NAME "votos_pipe"
#define RESULT_PIPE "resultado_pipe"

int main() {
    int num_jugadores;

    // Abrir el pipe de votos para leer
    int pipe_fd = open(PIPE_NAME, O_RDONLY);
    if (pipe_fd == -1) {
        perror("Error abriendo el pipe de votos");
        exit(EXIT_FAILURE);
    }

    // Leer el número de jugadores
    read(pipe_fd, &num_jugadores, sizeof(int));

    // Crear arreglo dinámico para contar los votos
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

    // Enviar el jugador más votado a través del pipe de resultados
    int result_pipe_fd = open(RESULT_PIPE, O_WRONLY);
    if (result_pipe_fd == -1) {
        perror("Error abriendo el pipe de resultados");
        exit(EXIT_FAILURE);
    }

    write(result_pipe_fd, &jugador_eliminado, sizeof(int));
    close(result_pipe_fd);

    free(votos); // Liberar la memoria asignada para los votos
    return 0;
}
