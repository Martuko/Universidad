#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <time.h>
#include <sys/mman.h>
#include <unistd.h>

#define PIPE_NAME_READ "votos_pipe"

typedef struct {
    int N;
    int jugador_mas_votado;
} DatosCompartidos;

void llenar_con_ceros(int votos[], int N) {
    for (int i = 0; i < N; i++) {
        votos[i] = 0;
    }
}

int main() {
    unlink(PIPE_NAME_READ);
    mkfifo(PIPE_NAME_READ, 0666);

    int pipe_fd = open(PIPE_NAME_READ, O_RDONLY);
    if (pipe_fd == -1) {
        perror("Error abriendo el pipe de votos");
        exit(1);
    }

    const char *name = "/mi_memoria_compartida";
    int shm_fd;
    DatosCompartidos *ptr;

    shm_fd = shm_open(name, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        perror("Error al abrir la memoria compartida");
        exit(1);
    }

    ftruncate(shm_fd, sizeof(DatosCompartidos));

    ptr = mmap(0, sizeof(DatosCompartidos), PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (ptr == MAP_FAILED) {
        perror("Error al mapear la memoria compartida");
        exit(1);
    }

    while (ptr->N > 1) {
        int votos[ptr->N];
        llenar_con_ceros(votos, ptr->N);
        int voto;

        printf("Esperando votos...\n");
        for (int i = 0; i < ptr->N; i++) {
            if (read(pipe_fd, &voto, sizeof(int)) <= 0) {
                printf("Error al leer voto.\n");
                ptr->N = 1; // Finaliza si hay un error
                break;
            }

            if (voto >= 0 && voto < ptr->N) {
                votos[voto]++;
            } else {
                printf("Voto fuera de rango: %d\n", voto);
            }
        }

        // Determinar el jugador más votado
        int max_votos = 0, jugador_eliminado = -1;
        for (int i = 0; i < ptr->N; i++) {
            if (votos[i] > max_votos) {
                max_votos = votos[i];
                jugador_eliminado = i + 1; // Ajustar el índice correctamente
            }
        }

        // Validar el jugador a eliminar
        if (jugador_eliminado == -1) {
            printf("Error: no se pudo determinar el jugador a eliminar.\n");
            break;
        }

        printf("El jugador %d fue el más votado y será eliminado.\n", jugador_eliminado);
        ptr->jugador_mas_votado = jugador_eliminado;
    }

    close(pipe_fd);
    munmap(ptr, sizeof(DatosCompartidos));
    close(shm_fd);

    printf("¡Tenemos un ganador!\n");
    return 0;
}
