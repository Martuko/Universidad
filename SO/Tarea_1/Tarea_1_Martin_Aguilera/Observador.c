#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <sys/mman.h>
#include <semaphore.h>

#define PIPE_NAME "votos_pipe"
#define RESULT_PIPE "resultado_pipe"
#define SHARED_MEM_NAME "/mem_jugadores"

typedef struct {
    int num_jugadores;
    int votos_completados;
} SharedData;

SharedData *shared_data;
sem_t *sem_sync;

void contar_votos(int num_jugadores);

int main() {
    int shm_fd = shm_open(SHARED_MEM_NAME, O_RDWR, 0666);
    if (shm_fd == -1) {
        perror("Error accediendo a la memoria compartida");
        exit(EXIT_FAILURE);
    }
    shared_data = (SharedData *)mmap(0, sizeof(SharedData), PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (shared_data == MAP_FAILED) {
        perror("Error mapeando la memoria compartida");
        exit(EXIT_FAILURE);
    }

    sem_sync = sem_open("/sem_sync", 0);
    if (sem_sync == SEM_FAILED) {
        perror("Error abriendo semáforo");
        exit(EXIT_FAILURE);
    }

    while (shared_data->num_jugadores > 1) {
        while (1) {
            sem_wait(sem_sync);
            if (shared_data->votos_completados == shared_data->num_jugadores) {
                sem_post(sem_sync);
                break;
            }
            sem_post(sem_sync);
            usleep(100000);
        }

        contar_votos(shared_data->num_jugadores);
    }

    printf("Observador: ¡El juego ha terminado!\n");

    munmap(shared_data, sizeof(SharedData));
    shm_unlink(SHARED_MEM_NAME);
    sem_close(sem_sync);
    sem_unlink("/sem_sync");

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
    while (votos_recibidos < num_jugadores) {
        if (read(pipe_fd, &voto, sizeof(int)) > 0) {
            if (voto >= 1 && voto <= num_jugadores) {
                votos[voto]++;
                votos_recibidos++;
                printf("Observador: Jugador %d recibió un voto.\n", voto);
            }
        } else {
            usleep(100000);
        }
    }
    close(pipe_fd);

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

    if (num_empatados > 1) {
        srand(time(NULL));
        jugador_eliminado = jugadores_empatados[rand() % num_empatados];
        printf("Observador: Empate en los votos, eliminando aleatoriamente al jugador %d.\n", jugador_eliminado);
    }

    printf("Observador: Jugador %d fue el más votado y será eliminado.\n", jugador_eliminado);

    int result_pipe_fd = open(RESULT_PIPE, O_WRONLY);
    if (result_pipe_fd == -1) {
        perror("Error abriendo el pipe de resultados");
        exit(EXIT_FAILURE);
    }
    write(result_pipe_fd, &jugador_eliminado, sizeof(int));
    close(result_pipe_fd);

    unlink(PIPE_NAME);
    unlink(RESULT_PIPE);
    mkfifo(PIPE_NAME, 0666);
    mkfifo(RESULT_PIPE, 0666);
}
