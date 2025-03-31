#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <semaphore.h>

#define PIPE_NAME "votos_pipe"
#define RESULT_PIPE "resultado_pipe"
#define SHARED_MEM_NAME "/mem_jugadores"

typedef struct {
    int num_jugadores;
    int votos_completados;
} SharedData;

int sincronizacion_pipes[10][2];
int confirmacion_pipes[10][2];
pid_t jugadores_pids[10];
SharedData *shared_data;
sem_t *sem_sync;

void crear_jugadores();
void votar();
void eliminar_jugador(int jugador_eliminado);
void jugador(int id);
void iniciar_votacion(int id);
void recrear_pipes();
void limpiar_pipes();
void verificar_pipes();

int main() {
    int shm_fd = shm_open(SHARED_MEM_NAME, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        perror("Error creando memoria compartida");
        exit(EXIT_FAILURE);
    }
    ftruncate(shm_fd, sizeof(SharedData));
    shared_data = (SharedData *)mmap(0, sizeof(SharedData), PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (shared_data == MAP_FAILED) {
        perror("Error mapeando memoria compartida");
        exit(EXIT_FAILURE);
    }
    shared_data->num_jugadores = 10;
    shared_data->votos_completados = 0;
    sem_sync = sem_open("/sem_sync", O_CREAT, 0666, 1);

    recrear_pipes();
    printf("Ejecuta el Observador en otra terminal antes de continuar.\n");

    crear_jugadores();

    while (shared_data->num_jugadores > 1) {
        votar();
        int jugador_eliminado;
        int result_pipe_fd = open(RESULT_PIPE, O_RDONLY);
        if (result_pipe_fd == -1) {
            perror("Error abriendo el pipe de resultados");
            exit(EXIT_FAILURE);
        }
        read(result_pipe_fd, &jugador_eliminado, sizeof(int));
        close(result_pipe_fd);
        eliminar_jugador(jugador_eliminado);
        limpiar_pipes();
        verificar_pipes();
        sleep(1);
    }

    unlink(PIPE_NAME);
    unlink(RESULT_PIPE);
    munmap(shared_data, sizeof(SharedData));
    shm_unlink(SHARED_MEM_NAME);
    sem_close(sem_sync);
    sem_unlink("/sem_sync");
    return 0;
}

void crear_jugadores() {
    for (int i = 0; i < shared_data->num_jugadores; i++) {
        if (pipe(sincronizacion_pipes[i]) == -1 || pipe(confirmacion_pipes[i]) == -1) {
            perror("Error creando pipes de sincronización");
            exit(EXIT_FAILURE);
        }

        jugadores_pids[i] = fork();
        if (jugadores_pids[i] == 0) {
            close(sincronizacion_pipes[i][1]);
            close(confirmacion_pipes[i][0]);
            jugador(i + 1);
            exit(0);
        }
        close(sincronizacion_pipes[i][0]);
        close(confirmacion_pipes[i][1]);
    }
}

void votar() {
    char mensaje[] = "VOTAR";
    sem_wait(sem_sync);
    shared_data->votos_completados = 0;
    sem_post(sem_sync);

    for (int i = 0; i < shared_data->num_jugadores; i++) {
        write(sincronizacion_pipes[i][1], mensaje, sizeof(mensaje));
        char confirmacion[10];
        read(confirmacion_pipes[i][0], confirmacion, sizeof(confirmacion));
    }
}

void eliminar_jugador(int jugador_eliminado) {
    int index = jugador_eliminado - 1;
    if (index >= 0 && index < shared_data->num_jugadores) {
        char mensaje[] = "ELIMINAR";
        write(sincronizacion_pipes[index][1], mensaje, sizeof(mensaje));
        char confirmacion[10];
        read(confirmacion_pipes[index][0], confirmacion, sizeof(confirmacion));

        for (int i = index; i < shared_data->num_jugadores - 1; i++) {
            jugadores_pids[i] = jugadores_pids[i + 1];
            sincronizacion_pipes[i][0] = sincronizacion_pipes[i + 1][0];
            sincronizacion_pipes[i][1] = sincronizacion_pipes[i + 1][1];
            confirmacion_pipes[i][0] = confirmacion_pipes[i + 1][0];
            confirmacion_pipes[i][1] = confirmacion_pipes[i + 1][1];
        }
        sem_wait(sem_sync);
        shared_data->num_jugadores--;
        sem_post(sem_sync);
    }
}

void jugador(int id) {
    printf("Jugador %d está listo.\n", id);

    while (1) {
        char buffer[10];
        read(sincronizacion_pipes[id - 1][0], buffer, sizeof(buffer));

        if (strcmp(buffer, "VOTAR") == 0) {
            iniciar_votacion(id);
        } else if (strcmp(buffer, "ELIMINAR") == 0) {
            write(confirmacion_pipes[id - 1][1], "OK", 3);
            execl("./Amurrado", "Amurrado", NULL);
            exit(0);
        }
    }
}

void iniciar_votacion(int id) {
    int pipe_fd = open(PIPE_NAME, O_WRONLY);
    if (pipe_fd == -1) {
        perror("Error abriendo el pipe de votos");
        exit(EXIT_FAILURE);
    }

    srand(time(NULL) + getpid());
    int voto = (rand() % shared_data->num_jugadores) + 1;
    write(pipe_fd, &voto, sizeof(voto));
    close(pipe_fd);

    sem_wait(sem_sync);
    shared_data->votos_completados++;
    sem_post(sem_sync);

    write(confirmacion_pipes[id - 1][1], "OK", 3);
}

void recrear_pipes() {
    if (access(PIPE_NAME, F_OK) == -1) {
        if (mkfifo(PIPE_NAME, 0666) == -1) {
            perror("Error creando PIPE_NAME");
            exit(EXIT_FAILURE);
        }
    }
    if (access(RESULT_PIPE, F_OK) == -1) {
        if (mkfifo(RESULT_PIPE, 0666) == -1) {
            perror("Error creando RESULT_PIPE");
            exit(EXIT_FAILURE);
        }
    }
}

void limpiar_pipes() {
    char buffer[100];
    int fd = open(PIPE_NAME, O_RDONLY | O_NONBLOCK);
    if (fd != -1) {
        while (read(fd, buffer, sizeof(buffer)) > 0);
        close(fd);
    }

    fd = open(RESULT_PIPE, O_RDONLY | O_NONBLOCK);
    if (fd != -1) {
        while (read(fd, buffer, sizeof(buffer)) > 0);
        close(fd);
    }
}

void verificar_pipes() {
    char buffer[100];
    int fd = open(PIPE_NAME, O_RDONLY | O_NONBLOCK);
    if (fd != -1) {
        read(fd, buffer, sizeof(buffer));
        close(fd);
    }

    fd = open(RESULT_PIPE, O_RDONLY | O_NONBLOCK);
    if (fd != -1) {
        read(fd, buffer, sizeof(buffer));
        close(fd);
    }
}
