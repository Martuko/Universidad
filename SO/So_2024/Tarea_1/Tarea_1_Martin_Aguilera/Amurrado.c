#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    printf("El jugador con PID %d se amurra y se retira del juego.\n", getpid());
    exit(0);
    return 0;
}
