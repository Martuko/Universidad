#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <time.h>

#define PROFESORES_POR_PLATAFORMA 6
#define DURACION_MES 4
#define DURACION_6_MESES 24
#define DURACION_ANO 48

// Variables globales
int seriesDasney = 0, seriesBetflix = 0;
sem_t semDasney, semBetflix;

// Genera un número aleatorio en un rango específico
float generar_aleatorio(float min, float max) {
    return min + ((float)rand() / RAND_MAX) * (max - min);
}

// Función para simular las series de Dasney
void *simularDasney(void *arg) {
    int semanas = *(int *)arg;
    for (int semana = 0; semana < semanas; semana++) {
        sem_wait(&semDasney);
        seriesDasney = (int)generar_aleatorio(10, 15);
        printf("Dasney lanza %d series en la semana %d\n", seriesDasney, semana + 1);
        sem_post(&semDasney);
        sleep(1); // Simula el paso de una semana
    }
    return NULL;
}

// Función para simular las series de Betflix
void *simularBetflix(void *arg) {
    int semanas = *(int *)arg;
    for (int semana = 0; semana < semanas; semana++) {
        sem_wait(&semBetflix);
        seriesBetflix = (int)generar_aleatorio(10, 15);
        printf("Betflix lanza %d series en la semana %d\n", seriesBetflix, semana + 1);
        sem_post(&semBetflix);
        sleep(1); // Simula el paso de una semana
    }
    return NULL;
}

// Función que simula la actividad de un profesor
void *profesor(void *arg) {
    int id = *(int *)arg;
    float totalSeriesVistas = 0;
    int semanas = *(int *)(arg + sizeof(int)); // Número de semanas

    for (int semana = 0; semana < semanas; semana++) {
        float series = generar_aleatorio(0.5, 2.0);
        totalSeriesVistas += series;

        if (id < PROFESORES_POR_PLATAFORMA) {
            sem_wait(&semDasney);
            printf("Profesor %d (Dasney) ve %.1f series\n", id + 1, series);
            sem_post(&semDasney);
        } else {
            sem_wait(&semBetflix);
            printf("Profesor %d (Betflix) ve %.1f series\n", id + 1, series);
            sem_post(&semBetflix);
        }
        sleep(1); // Simula el paso de una semana
    }

    printf("Profesor %d ha visto un total de %.1f series.\n", id + 1, totalSeriesVistas);
    free(arg); // Libera la memoria asignada al ID
    return NULL;
}

// Función principal
int main() {
    srand(time(NULL));

    int duracion, opcion;
    printf("Seleccione la duración de la simulación:\n");
    printf("1. 1 mes\n2. 6 meses\n3. 1 año\n");
    scanf("%d", &opcion);

    switch (opcion) {
        case 1: duracion = DURACION_MES; break;
        case 2: duracion = DURACION_6_MESES; break;
        case 3: duracion = DURACION_ANO; break;
        default: printf("Opción no válida\n"); return 1;
    }

    pthread_t threadsDasney[PROFESORES_POR_PLATAFORMA];
    pthread_t threadsBetflix[PROFESORES_POR_PLATAFORMA];
    pthread_t threadSimDasney, threadSimBetflix;

    sem_init(&semDasney, 0, 1);
    sem_init(&semBetflix, 0, 1);

    // Crear hilos para las plataformas
    pthread_create(&threadSimDasney, NULL, simularDasney, &duracion);
    pthread_create(&threadSimBetflix, NULL, simularBetflix, &duracion);

    // Crear hilos para los profesores
    for (int i = 0; i < PROFESORES_POR_PLATAFORMA; i++) {
        int *arg = malloc(2 * sizeof(int)); // Alocar memoria para ID y semanas
        arg[0] = i;
        arg[1] = duracion;
        pthread_create(&threadsDasney[i], NULL, profesor, arg);
    }

    for (int i = 0; i < PROFESORES_POR_PLATAFORMA; i++) {
        int *arg = malloc(2 * sizeof(int));
        arg[0] = i + PROFESORES_POR_PLATAFORMA;
        arg[1] = duracion;
        pthread_create(&threadsBetflix[i], NULL, profesor, arg);
    }

    // Esperar a que terminen los hilos de las plataformas
    pthread_join(threadSimDasney, NULL);
    pthread_join(threadSimBetflix, NULL);

    // Esperar a que terminen los hilos de los profesores
    for (int i = 0; i < PROFESORES_POR_PLATAFORMA; i++) {
        pthread_join(threadsDasney[i], NULL);
        pthread_join(threadsBetflix[i], NULL);
    }

    // Destruir los semáforos
    sem_destroy(&semDasney);
    sem_destroy(&semBetflix);

    return 0;
}
