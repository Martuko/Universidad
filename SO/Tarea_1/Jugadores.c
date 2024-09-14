#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>

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
        pause();  // Espera activamente la señal
    }

    while (num_jugadores > 1) {
        printf("Todos los jugadores están listos. Iniciando la votación.\n");

        votar();

        int jugador_eliminado;
        int result_pipe_fd = open(RESULT_PIPE, O_RDONLY);
        read(result_pipe_fd, &jugador_eliminado, sizeof(int));
        close(result_pipe_fd);

        eliminar_jugador(jugador_eliminado);
        printf("Continua el juego con la siguiente ronda\n");

        recrear_pipes();
        verificar_pipes();
        sleep(1);
    }

    printf("¡El jugador final es el ganador!\n");
    unlink(PIPE_NAME);
    unlink(RESULT_PIPE);

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
    for (int i = 0; i < num_jugadores; i++) {
        kill(jugadores_pids[i], SIGCONT);
    }
}

void eliminar_jugador(int jugador_eliminado) {
    int index = jugador_eliminado - 1;
    if (index >= 0 && index < num_jugadores) {
        kill(jugadores_pids[index], SIGTERM);
        for (int i = index; i < num_jugadores - 1; i++) {
            jugadores_pids[i] = jugadores_pids[i + 1];
        }
        num_jugadores--;
    }
}

void jugador(int id) {
    signal(SIGCONT, iniciar_votacion);  // Usar signal en lugar de sigaction

    printf("Jugador %d está listo.\n", id);
    kill(getppid(), SIGUSR1);

    pause();  // Espera a que el proceso principal indique que la votación puede empezar
}

void iniciar_votacion(int sig) {
    (void)sig;  // Marcar como usado para evitar advertencia del compilador

    int pipe_fd = open(PIPE_NAME, O_WRONLY);
    srand(time(NULL) + getpid());
    int voto = (rand() % num_jugadores) + 1;
    write(pipe_fd, &voto, sizeof(voto));
    close(pipe_fd);

    pause();  // Esperar la siguiente señal de votación
}

void jugador_listo(int sig) {
    (void)sig;  // Marcar como usado para evitar advertencia del compilador
    jugadores_listos++;
}

void recrear_pipes() {
    unlink(PIPE_NAME);
    unlink(RESULT_PIPE);
    mkfifo(PIPE_NAME, 0666);
    mkfifo(RESULT_PIPE, 0666);
}

void verificar_pipes() {
    char buffer[100];
    int fd = open(PIPE_NAME, O_RDONLY | O_NONBLOCK);
    if (fd != -1) {
        if (read(fd, buffer, sizeof(buffer)) > 0) {
            printf("Contenido inesperado en %s.\n", PIPE_NAME);
        }
        close(fd);
    }

    fd = open(RESULT_PIPE, O_RDONLY | O_NONBLOCK);
    if (fd != -1) {
        if (read(fd, buffer, sizeof(buffer)) > 0) {
            printf("Contenido inesperado en %s.\n", RESULT_PIPE);
        }
        close(fd);
    }
}
