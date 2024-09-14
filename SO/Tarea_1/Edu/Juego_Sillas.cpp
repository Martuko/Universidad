#include <iostream>
#include <cstdlib>
#include <ctime>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <cstring>
#include <fcntl.h>
#include <sys/stat.h>
#include <cerrno>
#include <vector>

using namespace std;

const char *fifo_path1 = "./fifo_juego_a_observador";  // Para enviar votos al observador
const char *fifo_path2 = "./fifo_observador_a_juego";  // Para recibir resultado del observador

// Función para generar un número aleatorio
int generarNumeroAleatorio(int min, int max) {
    return min + rand() % (max - min + 1);
}

int main() {
    srand(time(NULL));  // Inicializar semilla aleatoria

    int n;
    cout << "Ingrese el número de jugadores: ";
    cin >> n;

    // Crear FIFOs si no existen
    mkfifo(fifo_path1, 0666);
    mkfifo(fifo_path2, 0666);

    // Crear un vector para guardar los PIDs de los jugadores
    vector<pid_t> jugadores(n);

    // Crear pipes para cada proceso hijo
    vector<vector<int>> pipefds(n, vector<int>(2));
    for (int i = 0; i < n; i++) {
        if (pipe(pipefds[i].data()) == -1) {
            cerr << "Error al crear el pipe para el jugador " << i + 1 << ": " << strerror(errno) << endl;
            exit(EXIT_FAILURE);
        }
    }

    // Crear procesos para los jugadores
    for (int i = 0; i < n; i++) {
        pid_t pid = fork();

        if (pid < 0) {
            cerr << "Error en fork" << endl;
            exit(EXIT_FAILURE);
        } else if (pid == 0) {  // Proceso hijo
            while (true) {  // Ciclo para que los jugadores sigan votando
                // Abrir FIFO para enviar votos al observador
                int fd_write = open(fifo_path1, O_WRONLY);
                if (fd_write == -1) {
                    cerr << "Error al abrir FIFO para escritura (fifo_juego_a_observador): " << strerror(errno) << endl;
                    exit(EXIT_FAILURE);
                }

                int voto = generarNumeroAleatorio(1, n);
                write(fd_write, &voto, sizeof(voto));
                cout << "Proceso hijo " << getpid() << " envió su voto: " << voto << endl;
                close(fd_write);

                // Esperar el jugador con más votos
                close(pipefds[i][1]);  // Cerramos el lado de escritura de este pipe en el hijo
                int jugadorConMasVotos;

                if (read(pipefds[i][0], &jugadorConMasVotos, sizeof(jugadorConMasVotos)) == sizeof(jugadorConMasVotos)) {
                    cout << "Proceso hijo " << getpid() << " recibió el jugador con más votos: " << jugadorConMasVotos << endl;

                    // Si el proceso hijo es el jugador con más votos, ejecuta el programa Se_Amurra
                    if (i + 1 == jugadorConMasVotos) {
                        execlp("./Se_Amurra", "", NULL);
                    }
                } else {
                    cerr << "Error al leer el jugador con más votos en el proceso hijo " << getpid() << endl;
                }

                close(pipefds[i][0]);  // Cerrar la lectura en el hijo
                exit(0);
            }
        } else {
            jugadores[i] = pid;  // Guardar el PID del proceso hijo
        }
    }

    // Ciclo de votaciones hasta que quede un solo jugador
    while (jugadores.size() > 1) {
        int fd_write = open(fifo_path1, O_WRONLY);
        if (fd_write == -1) {
            cerr << "Error al abrir FIFO para escritura (fifo_juego_a_observador): " << strerror(errno) << endl;
            exit(EXIT_FAILURE);
        }

        int num_jugadores = jugadores.size();
        write(fd_write, &num_jugadores, sizeof(num_jugadores));
        close(fd_write);

        int fd_read = open(fifo_path2, O_RDONLY);
        if (fd_read == -1) {
            cerr << "Error al abrir FIFO para lectura (fifo_observador_a_juego): " << strerror(errno) << endl;
            exit(EXIT_FAILURE);
        }

        int jugadorConMasVotos;
        read(fd_read, &jugadorConMasVotos, sizeof(jugadorConMasVotos));
        close(fd_read);

        cout << "Jugador con más votos: " << jugadorConMasVotos << endl;

        // Enviar el jugador con más votos a todos los procesos hijos a través de sus respectivos pipes
        for (int i = 0; i < jugadores.size(); i++) {
            close(pipefds[i][0]);  // Cerrar la lectura en el padre
            write(pipefds[i][1], &jugadorConMasVotos, sizeof(jugadorConMasVotos));  // Enviar el valor del jugador
            close(pipefds[i][1]);  // Cerrar la escritura en el padre
        }

        // Esperar a que los hijos terminen su ejecución
        for (int i = 0; i < jugadores.size(); i++) {
            waitpid(jugadores[i], NULL, 0);
        }

        // Eliminar el jugador con más votos del vector de jugadores
        jugadores.erase(jugadores.begin() + (jugadorConMasVotos - 1));
    }

    if (!jugadores.empty()) {
        cout << "¡El jugador " << jugadores.front() << " es el ganador!" << endl;
    } else {
        cout << "Error: No hay jugadores en la lista." << endl;
    }

    return 0;
}
