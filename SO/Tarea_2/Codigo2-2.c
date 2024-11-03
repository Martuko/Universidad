#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>
#include <unistd.h> // Biblioteca para usar sleep()

#define NUM_PROFESORES 12
#define SERIES_MIN 10
#define SERIES_MAX 15

typedef struct {
    int id;
    char *plataforma;
    int semanas;
} Profesor;

pthread_mutex_t mutex;
int seriesDasney = 0;
int seriesBetflix = 0;

// Función para generar nuevas series
void generarSeries(int *series, const char *plataforma) {
    int nuevasSeries = rand() % (SERIES_MAX - SERIES_MIN + 1) + SERIES_MIN;
    *series += nuevasSeries;
    printf("[DEBUG] Se generaron %d series nuevas en %s. Total ahora: %d\n", nuevasSeries, plataforma, *series);
}

// Función que simula el comportamiento de un profesor con livelock
void *verSeries(void *arg) {
    Profesor *profesor = (Profesor *)arg;
    for (int semana = 0; semana < profesor->semanas; semana++) {
        float seriesPorSemana = (rand() % 4 + 1) * 0.5;
        int intentos = 0;

        while (intentos < 5) { // Intentar varias veces sin progreso
            pthread_mutex_lock(&mutex);
            if (profesor->plataforma == "Dasney" && seriesDasney > 0) {
                if (seriesDasney >= (int)seriesPorSemana) {
                    seriesDasney -= (int)seriesPorSemana;
                    printf("[DEBUG] Profesor %d ve %.1f series en Dasney.\n", profesor->id, seriesPorSemana);
                    pthread_mutex_unlock(&mutex);
                    break; // Progreso realizado, salir del ciclo
                } else {
                    printf("[DEBUG] Profesor %d no pudo ver series suficientes en Dasney, intentando de nuevo...\n", profesor->id);
                }
            } else if (profesor->plataforma == "Betflix" && seriesBetflix > 0) {
                if (seriesBetflix >= (int)seriesPorSemana) {
                    seriesBetflix -= (int)seriesPorSemana;
                    printf("[DEBUG] Profesor %d ve %.1f series en Betflix.\n", profesor->id, seriesPorSemana);
                    pthread_mutex_unlock(&mutex);
                    break; // Progreso realizado, salir del ciclo
                } else {
                    printf("[DEBUG] Profesor %d no pudo ver series suficientes en Betflix, intentando de nuevo...\n", profesor->id);
                }
            }
            pthread_mutex_unlock(&mutex);
            intentos++;
            usleep(100000); // Pequeña espera antes de volver a intentar (simula livelock)
        }
        sleep(1); // Simular tiempo de espera de una semana
    }
    pthread_exit(NULL);
}

int main() {
    srand(time(NULL));
    pthread_t threads[NUM_PROFESORES];
    Profesor profesores[NUM_PROFESORES];
    pthread_mutex_init(&mutex, NULL);

    int meses;
    printf("Ingrese el tiempo de ejecución en meses (1, 6, 12): ");
    scanf("%d", &meses);

    int semanas = meses * 4; // 4 semanas por mes

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
        pthread_mutex_lock(&mutex);
        generarSeries(&seriesDasney, "Dasney");
        generarSeries(&seriesBetflix, "Betflix");
        pthread_mutex_unlock(&mutex);
        sleep(1); // Simular tiempo de espera de una semana
    }

    // Esperar a que terminen todos los threads
    for (int i = 0; i < NUM_PROFESORES; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&mutex);
    printf("Simulación completada.\n");
    return 0;
}
