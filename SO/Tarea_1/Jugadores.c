#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>
#include <sys/wait.h>

#define PIPE_NAME "votos_pipe"
#define RESULT_PIPE "resultado_pipe"

int num_jugadores = 10;
volatile sig_atomic_t jugadores_listos = 0;
pid_t jugadores_pids[10];

void crear_jugadores();
void votar();
void eliminar_jugador(int jugador_eliminado);
void jugador(int id);
void jugador_listo(int sig);
void iniciar_votacion(int sig);
void recrear_pipes();
void verificar_pipes();

int main() {
    struct sigaction sa;
    sa.sa_handler = jugador_listo;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGUSR1, &sa, NULL);

    recrear_pipes();

    pid_t observador_pid = fork();
    if (observador_pid == 0) {
        execl("./Observador", "Observador", NULL);
        perror("Error ejecutando el Observador");
        exit(EXIT_FAILURE);
    } else if (observador_pid < 0) {
        perror("Error creando el proceso Observador");
        exit(EXIT_FAILURE);
    }

    crear_jugadores();

    while (jugadores_listos < num_jugadores) {
        pause();
    }

    while (num_jugadores > 1) {
        printf("Todos los jugadores están listos. Iniciando la votación.\n");

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
        printf("Continúa el juego con la siguiente ronda.\n");

        recrear_pipes();
        verificar_pipes();
        sleep(1);
    }

    printf("¡El jugador final es el ganador!\n");
    // Eliminar los pipes al finalizar
    system("rm -f " PIPE_NAME);
    system("rm -f " RESULT_PIPE);

    return 0;
}

void crear_jugadores() {
    for (int i = 0; i < num_jugadores; i++) {
        jugadores_pids[i] = fork();
        if (jugadores_pids[i] == 0) {
            jugador(i + 1);
            exit(0);
        }
    }
}

void votar() {
    printf("Enviando señales de votación a cada jugador...\n");
    for (int i = 0; i < num_jugadores; i++) {
        printf("Enviando señal SIGCONT al jugador con PID %d.\n", jugadores_pids[i]);
        if (kill(jugadores_pids[i], SIGCONT) < 0) {
            perror("Error enviando señal SIGCONT");
        }
    }
}

void eliminar_jugador(int jugador_eliminado) {
    int index = jugador_eliminado - 1;
    if (index >= 0 && index < num_jugadores) {
        printf("Eliminando jugador %d con PID %d.\n", jugador_eliminado, jugadores_pids[index]);

        if (fork() == 0) {
            execl("./Amurrado", "Amurrado", NULL);
            perror("Error ejecutando Amurrado");
            exit(EXIT_FAILURE);
        }
        wait(NULL);

        for (int i = index; i < num_jugadores - 1; i++) {
            jugadores_pids[i] = jugadores_pids[i + 1];
        }
        jugadores_pids[num_jugadores - 1] = 0;
        num_jugadores--;

        printf("Número de jugadores restantes: %d\n", num_jugadores);
    } else {
        printf("Índice de jugador eliminado fuera de rango.\n");
    }
}

void jugador(int id) {
    struct sigaction sa;
    sa.sa_handler = iniciar_votacion;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGCONT, &sa, NULL);

    printf("Jugador %d está listo.\n", id);
    kill(getppid(), SIGUSR1);

    while (1) {
        pause();
    }
}

void iniciar_votacion(int sig) {
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

    printf("Jugador con PID %d ha completado la votación y espera la siguiente ronda...\n", getpid());
}

void jugador_listo(int sig) {
    jugadores_listos++;
}

void recrear_pipes() {
    system("rm -f " PIPE_NAME);
    system("rm -f " RESULT_PIPE);
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
