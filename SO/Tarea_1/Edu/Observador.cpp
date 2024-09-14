#include <iostream>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <cstring>
#include <cerrno>
#include <map>

using namespace std;

const char *fifo_path1 = "./fifo_juego_a_observador";  // Para recibir votos del juego
const char *fifo_path2 = "./fifo_observador_a_juego";  // Para enviar resultado al juego

int main() {
    // Crear FIFOs si no existen
    mkfifo(fifo_path1, 0666);
    mkfifo(fifo_path2, 0666);

    while (true) {  // Ciclo infinito para continuar el juego
        // Abrir FIFO para leer los votos del juego
        int fd_read = open(fifo_path1, O_RDONLY);
        if (fd_read == -1) {
            cerr << "Error al abrir FIFO para lectura (fifo_juego_a_observador): " << strerror(errno) << endl;
            exit(EXIT_FAILURE);
        }

        int n;
        read(fd_read, &n, sizeof(n));  // Leer el número de jugadores
        cout << "Número de jugadores leído desde FIFO (fifo_juego_a_observador): " << n << endl;

        // Mapa para contar votos
        map<int, int> votos;

        // Leer los votos de los jugadores
        for (int i = 0; i < n; i++) {
            int voto;
            read(fd_read, &voto, sizeof(voto));
            cout << "Voto leído desde FIFO (fifo_juego_a_observador): " << voto << endl;
            votos[voto]++;
        }

        close(fd_read);  // Cerrar lectura de FIFO

        // Determinar el jugador con más votos
        int jugadorConMasVotos = -1;
        int maxVotos = 0;
        for (auto &entry : votos) {
            if (entry.second > maxVotos) {
                maxVotos = entry.second;
                jugadorConMasVotos = entry.first;
            }
        }

        cout << "Jugador con más votos: " << jugadorConMasVotos << " con " << maxVotos << " votos." << endl;

        // Abrir FIFO para enviar el jugador con más votos al juego (sin O_NONBLOCK)
        int fd_write = open(fifo_path2, O_WRONLY);  // Sin O_NONBLOCK
        if (fd_write == -1) {
            cerr << "Error al abrir FIFO para escritura (fifo_observador_a_juego): " << strerror(errno) << endl;
            exit(EXIT_FAILURE);
        }

        // Enviar el jugador con más votos al juego
        write(fd_write, &jugadorConMasVotos, sizeof(jugadorConMasVotos));
        cout << "Jugador con más votos enviado al juego: " << jugadorConMasVotos << endl;

        close(fd_write);  // Cerrar escritura de FIFO
    }

    return 0;
}
