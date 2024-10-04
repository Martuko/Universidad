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
#include <sys/types.h>

#define PIPE_NAME_WRITE "votos_pipe"

typedef struct {
    int N;
    int jugador_mas_votado;
    pid_t jugadores[100]; // PIDs de jugadores activos
} DatosCompartidos;

void Crear_jugadores(int N, DatosCompartidos *ptr) {
    for (int i = 1; i < N; i++) {
        pid_t jugador = fork();

        if (jugador == 0) {
            // Código del jugador: Espera a ser eliminado
            while (1) {
                pause(); // El jugador espera hasta que sea eliminado
            }
        } else if (jugador > 0) {
            // Proceso padre guarda el PID del jugador
            ptr->jugadores[i] = jugador;
            printf("Jugador %d creado (PID: %d)\n", i + 1, jugador);
        } else {
            perror("Error al crear jugador");
            exit(1);
        }
    }
}

void votar(int pipe_fd, DatosCompartidos *ptr) {
    srand(time(NULL) + getpid());
    int voto = rand() % ptr->N;
    write(pipe_fd, &voto, sizeof(int));
}

int main() {
    unlink(PIPE_NAME_WRITE);

    const char *name = "/mi_memoria_compartida";
    int shm_fd;
    DatosCompartidos *ptr;

    // Inicializar la memoria compartida
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

    // Capturar el número de jugadores
    printf("Introduce la cantidad de jugadores: ");
    scanf("%d", &ptr->N);

    // Asignar el proceso principal al primer jugador
    ptr->jugadores[0] = getpid();

    Crear_jugadores(ptr->N, ptr);

    mkfifo(PIPE_NAME_WRITE, 0666);
    int pipe_fd = open(PIPE_NAME_WRITE, O_WRONLY);

    while (ptr->N > 1) {
        votar(pipe_fd, ptr);
        sleep(2);

        // Leer el jugador más votado desde la memoria compartida
        int jugador_eliminado = ptr->jugador_mas_votado;

        if (jugador_eliminado <= 0 || jugador_eliminado > ptr->N) {
            printf("Error: jugador eliminado fuera de rango: %d\n", jugador_eliminado);
            break;
        }

        pid_t pid_a_eliminar = ptr->jugadores[jugador_eliminado - 1];
        printf("Jugador %d con PID %d ha sido eliminado.\n", jugador_eliminado, pid_a_eliminar);

        // Eliminar al jugador
        kill(pid_a_eliminar, SIGKILL);
        waitpid(pid_a_eliminar, NULL, 0);

        // Ajustar la lista de PIDs de jugadores activos
        for (int i = jugador_eliminado - 1; i < ptr->N - 1; i++) {
            ptr->jugadores[i] = ptr->jugadores[i + 1];
        }

        ptr->N--; // Reducir el número de jugadores
    }

    close(pipe_fd);
    munmap(ptr, sizeof(DatosCompartidos));
    close(shm_fd);

    return 0;
}
