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
volatile sig_atomic_t votos_confirmados = 0;
pid_t jugadores_pids[10];

void crear_jugadores();
void votar();
void eliminar_jugador(int jugador_eliminado);
void jugador(int id);
void jugador_listo(int sig);
void iniciar_votacion(int sig);
void confirmar_voto(int sig);
void recrear_pipes();
void esperar_jugadores_listos();
void esperar_votacion_completa();

int main() {
    struct sigaction sa;
    sa.sa_handler = jugador_listo;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGUSR1, &sa, NULL);

    struct sigaction sa_confirm;
    sa_confirm.sa_handler = confirmar_voto;
    sigemptyset(&sa_confirm.sa_mask);
    sa_confirm.sa_flags = 0;
    sigaction(SIGUSR2, &sa_confirm, NULL);

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

    esperar_jugadores_listos();

    while (num_jugadores > 1) {
        printf("Todos los jugadores están listos. Iniciando la votación.\n");

        votos_confirmados = 0;  // Reiniciar contador de votos confirmados

        votar();

        esperar_votacion_completa();

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
        num_jugadores--;
        printf("Número de jugadores restantes: %d\n", num_jugadores);
    } else {
        printf("Índice de jugador eliminado fuera de rango.\n");
    }
}

void jugador(int id) {
    signal(SIGCONT, iniciar_votacion);
    signal(SIGUSR2, confirmar_voto);

    printf("Jugador %d está listo.\n", id);
    kill(getppid(), SIGUSR1);

    while (1) {
        pause();
    }
}

void iniciar_votacion(int sig) {
    printf("Jugador con PID %d está votando...\n", getpid());

    int pipe_fd;
    int retries = 5;
    while ((pipe_fd = open(PIPE_NAME, O_WRONLY)) == -1 && retries > 0) {
        perror("Error abriendo el pipe de votos, reintentando...");
        retries--;
        usleep(100000);
    }

    if (pipe_fd == -1) {
        perror("Error crítico al abrir el pipe de votos, saliendo...");
        exit(EXIT_FAILURE);
    }

    srand(time(NULL) + getpid());
    int voto = (rand() % num_jugadores) + 1;
    printf("Jugador con PID %d votó por el jugador %d.\n", getpid(), voto);

    if (write(pipe_fd, &voto, sizeof(voto)) == -1) {
        perror("Error escribiendo el voto en el pipe");
        close(pipe_fd);
        exit(EXIT_FAILURE);
    }

    if (close(pipe_fd) == -1) {
        perror("Error cerrando el pipe de votos");
    } else {
        printf("Jugador con PID %d cerró correctamente el pipe después de votar.\n", getpid());
    }

    printf("Jugador con PID %d ha completado la votación y espera confirmación...\n", getpid());
}

void confirmar_voto(int sig) {
    printf("Jugador con PID %d recibió confirmación de voto.\n", getpid());
    kill(getppid(), SIGUSR2);  // Notificar al proceso principal de la confirmación
}

void jugador_listo(int sig) {
    jugadores_listos++;
}

void recrear_pipes() {
    unlink(PIPE_NAME);
    unlink(RESULT_PIPE);

    if (mkfifo(PIPE_NAME, 0666) == -1) {
        perror("Error creando PIPE_NAME");
        exit(EXIT_FAILURE);
    }
    if (mkfifo(RESULT_PIPE, 0666) == -1) {
        perror("Error creando RESULT_PIPE");
        exit(EXIT_FAILURE);
    }
    printf("Pipes recreados correctamente para la nueva ronda.\n");
}

void esperar_jugadores_listos() {
    while (jugadores_listos < num_jugadores) {
        pause();
    }
}

void esperar_votacion_completa() {
    while (votos_confirmados < num_jugadores) {
        pause();
    }
    printf("Todos los votos confirmados para esta ronda.\n");
}
