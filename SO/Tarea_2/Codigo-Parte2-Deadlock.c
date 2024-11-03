//Deadlock Parte 2


#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h>

#define NUM_PROFESORES 12
#define SERIES_MIN 10
#define SERIES_MAX 15

typedef struct {
    int id;
    char *plataforma;
    int semanas;
} Profesor;

pthread_mutex_t mutexDasney;
pthread_mutex_t mutexBetflix;
int seriesDasney = 0;
int seriesBetflix = 0;

void generarSeries(int *series, const char *plataforma) {
    int nuevasSeries = rand() % (SERIES_MAX - SERIES_MIN + 1) + SERIES_MIN;
    *series += nuevasSeries;
    printf("[DEBUG] Se generaron %d series nuevas en %s. Total ahora: %d\n", nuevasSeries, plataforma, *series);
}

// Función que simula el comportamiento de un profesor con deadlock
void *verSeries(void *arg) {
    Profesor *profesor = (Profesor *)arg;
    for (int semana = 0; semana <= profesor->semanas; semana++) {
        float seriesPorSemana = (rand() % 4 + 1) * 0.5;

        if (profesor->id % 2 == 0) {
            // Profesores con ID par: bloquean Dasney primero, luego Betflix
            pthread_mutex_lock(&mutexDasney);
            sleep(1); // Simular un pequeño retraso
            pthread_mutex_lock(&mutexBetflix);
        } else {
            // Profesores con ID impar: bloquean Betflix primero, luego Dasney
            pthread_mutex_lock(&mutexBetflix);
            sleep(1); // Simular un pequeño retraso
            pthread_mutex_lock(&mutexDasney);
        }

        // Simular el consumo de series
        printf("[DEBUG] Profesor %d ve %.1f series en %s.\n", profesor->id, seriesPorSemana, profesor->plataforma);

        // Desbloquear los mutexes
        pthread_mutex_unlock(&mutexDasney);
        pthread_mutex_unlock(&mutexBetflix);

        sleep(1); // Simular tiempo de espera de una semana
    }
    pthread_exit(NULL);
}

int main() {
    srand(time(NULL));
    pthread_t threads[NUM_PROFESORES];
    Profesor profesores[NUM_PROFESORES];
    pthread_mutex_init(&mutexDasney, NULL);
    pthread_mutex_init(&mutexBetflix, NULL);

    int meses;
    printf("Ingrese el tiempo de ejecución en meses (1, 6, 12): ");
    scanf("%d", &meses);

    int semanas = meses * 4;

    // Inicializar profesores y asignar plataformas y semanas
    for (int i = 0; i < NUM_PROFESORES; i++) {
        profesores[i].id = i;
        profesores[i].plataforma = (i < 6) ? "Dasney" : "Betflix";
        profesores[i].semanas = semanas;
        printf("[DEBUG] Profesor %d asignado a %s\n", i, profesores[i].plataforma);
    }

    // Crear threads
    for (int i = 0; i < NUM_PROFESORES; i++) {
        pthread_create(&threads[i], NULL, verSeries, (void *)&profesores[i]);
    }

    // Simulación de generación semanal de series
    for (int i = 0; i < semanas; i++) {
        pthread_mutex_lock(&mutexDasney);
        pthread_mutex_lock(&mutexBetflix);
        generarSeries(&seriesDasney, "Dasney");
        generarSeries(&seriesBetflix, "Betflix");
        pthread_mutex_unlock(&mutexBetflix);
        pthread_mutex_unlock(&mutexDasney);
        sleep(1);
    }

    // Esperar a que terminen todos los threads
    for (int i = 0; i < NUM_PROFESORES; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&mutexDasney);
    pthread_mutex_destroy(&mutexBetflix);
    printf("Simulación completada.\n");
    return 0;
}
