#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>

#define PIPE_NAME "votos_pipe"
#define RESULT_PIPE "resultado_pipe"

void contar_votos(int num_jugadores);

int main() {
    while (1) {
        // Contar votos y determinar el jugador eliminado
        contar_votos(10);  // Cambia '10' por el número actual de jugadores si es necesario
    }
    return 0;
}

void contar_votos(int num_jugadores) {
    int votos[num_jugadores + 1];  // Array para contar votos de cada jugador
    memset(votos, 0, sizeof(votos));  // Reiniciar conteo de votos

    // Abrir pipe para leer votos
    int pipe_fd = open(PIPE_NAME, O_RDONLY);
    if (pipe_fd == -1) {
        perror("Error abriendo el pipe de votos");
        exit(EXIT_FAILURE);
    }

    // Leer todos los votos de los jugadores
    int voto;
    while (read(pipe_fd, &voto, sizeof(int)) > 0) {
        if (voto >= 1 && voto <= num_jugadores) {
            votos[voto]++;
            printf("Observador: Jugador %d recibió un voto.\n", voto);
        }
    }
    close(pipe_fd);

    // Determinar el jugador con más votos
    int jugador_eliminado = 0;
    int max_votos = 0;
    for (int i = 1; i <= num_jugadores; i++) {
        if (votos[i] > max_votos) {
            max_votos = votos[i];
            jugador_eliminado = i;
        }
    }

    printf("Observador: Jugador %d fue el más votado y será eliminado.\n", jugador_eliminado);

    // Enviar el jugador eliminado al pipe de resultados
    int result_pipe_fd = open(RESULT_PIPE, O_WRONLY);
    if (result_pipe_fd == -1) {
        perror("Error abriendo el pipe de resultados");
        exit(EXIT_FAILURE);
    }
    write(result_pipe_fd, &jugador_eliminado, sizeof(int));
    close(result_pipe_fd);
}
