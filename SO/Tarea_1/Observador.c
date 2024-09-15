#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>

#define PIPE_NAME "votos_pipe"
#define RESULT_PIPE "resultado_pipe"

void contar_votos(int num_jugadores);

int main() {
    int num_jugadores = 10;  // Número inicial de jugadores

    while (num_jugadores > 1) {
        contar_votos(num_jugadores);  // Contar votos con el número actual de jugadores
        num_jugadores--;  // Reducir el número de jugadores después de cada eliminación
    }
    printf("Observador: ¡El juego ha terminado!\n");
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

    // Leer exactamente num_jugadores votos
    int voto;
    int votos_recibidos = 0;
    while (votos_recibidos < num_jugadores) {
        if (read(pipe_fd, &voto, sizeof(int)) > 0) {
            if (voto >= 1 && voto <= num_jugadores) {
                votos[voto]++;
                votos_recibidos++;
                printf("Observador: Jugador %d recibió un voto.\n", voto);
            }
        } else {
            usleep(100000);  // Espera un poco si no hay datos para evitar bloqueo
        }
    }
    close(pipe_fd);

    // Determinar el jugador con más votos
    int jugador_eliminado = 0;
    int max_votos = 0;
    int jugadores_empatados[num_jugadores];
    int num_empatados = 0;

    for (int i = 1; i <= num_jugadores; i++) {
        if (votos[i] > max_votos) {
            max_votos = votos[i];
            jugador_eliminado = i;
            num_empatados = 1;
            jugadores_empatados[0] = i;
        } else if (votos[i] == max_votos) {
            jugadores_empatados[num_empatados] = i;
            num_empatados++;
        }
    }

    // Si hay empate, seleccionar un jugador al azar
    if (num_empatados > 1) {
        srand(time(NULL));
        jugador_eliminado = jugadores_empatados[rand() % num_empatados];
        printf("Observador: Empate en los votos, eliminando aleatoriamente al jugador %d.\n", jugador_eliminado);
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

    // Recrear los pipes para la siguiente ronda
    unlink(PIPE_NAME);
    unlink(RESULT_PIPE);
    mkfifo(PIPE_NAME, 0666);
    mkfifo(RESULT_PIPE, 0666);
}
