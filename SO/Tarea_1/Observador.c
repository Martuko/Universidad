#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <signal.h>

#define PIPE_NAME "votos_pipe"
#define RESULT_PIPE "resultado_pipe"

void contar_votos(int num_jugadores);

int main() {
    while (1) {
        contar_votos(10);
    }
    return 0;
}

void contar_votos(int num_jugadores) {
    int votos[num_jugadores + 1];
    memset(votos, 0, sizeof(votos));

    int pipe_fd = open(PIPE_NAME, O_RDONLY);
    if (pipe_fd == -1) {
        perror("Error abriendo el pipe de votos");
        exit(EXIT_FAILURE);
    }

    int voto;
    int votos_recibidos = 0;
    while (read(pipe_fd, &voto, sizeof(int)) > 0) {
        if (voto >= 1 && voto <= num_jugadores) {
            votos[voto]++;
            printf("Observador: Jugador %d recibió un voto. Total votos recibidos: %d/%d\n", voto, ++votos_recibidos, num_jugadores);

            // Enviar confirmación al jugador
            kill(getppid(), SIGUSR2); // Asumiendo que cada voto corresponde a un PID que se registra para confirmación
        }
    }
    close(pipe_fd);

    int jugador_eliminado = 0;
    int max_votos = 0;
    for (int i = 1; i <= num_jugadores; i++) {
        if (votos[i] > max_votos) {
            max_votos = votos[i];
            jugador_eliminado = i;
        }
    }

    printf("Observador: Jugador %d fue el más votado y será eliminado.\n", jugador_eliminado);

    int result_pipe_fd = open(RESULT_PIPE, O_WRONLY);
    if (result_pipe_fd == -1) {
        perror("Error abriendo el pipe de resultados");
        exit(EXIT_FAILURE);
    }
    write(result_pipe_fd, &jugador_eliminado, sizeof(int));
    close(result_pipe_fd);
}
