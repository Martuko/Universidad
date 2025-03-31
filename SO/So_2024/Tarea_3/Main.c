#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define TRUE 1
#define FALSE 0

typedef struct Pagina {
    int id_proceso;
    int num_pagina;
    int num_marco;
    int presencia; 
    struct Pagina *siguiente;
} Pagina;

typedef struct Proceso {
    int id_proceso;
    int tamaño; 
    int num_paginas;
    Pagina *tabla_paginas;
    struct Proceso *siguiente;
} Proceso;

int memoria_fisica_kb;
int memoria_virtual_kb;
int tamaño_pagina_kb;
int marcos_totales_ram;
int marcos_ocupados_ram = 0;
int marcos_totales_swap;
int marcos_ocupados_swap = 0;

Pagina **marcos_ram;
Pagina **marcos_swap;

Proceso *lista_procesos = NULL;

int id_proceso_actual = 1;
int tiempo_ejecucion = 0;

typedef struct NodoCola {
    Pagina *pagina;
    struct NodoCola *siguiente;
} NodoCola;

NodoCola *frente_ram = NULL;
NodoCola *final_ram = NULL;

void encolar_pagina_ram(Pagina *pagina) {
    NodoCola *nuevo_nodo = (NodoCola *)malloc(sizeof(NodoCola));
    nuevo_nodo->pagina = pagina;
    nuevo_nodo->siguiente = NULL;
    if (final_ram == NULL) {
        frente_ram = nuevo_nodo;
    } else {
        final_ram->siguiente = nuevo_nodo;
    }
    final_ram = nuevo_nodo;
}

Pagina *desencolar_pagina_ram() {
    if (frente_ram == NULL) {
        return NULL;
    }
    NodoCola *nodo_a_eliminar = frente_ram;
    Pagina *pagina = nodo_a_eliminar->pagina;
    frente_ram = frente_ram->siguiente;
    if (frente_ram == NULL) {
        final_ram = NULL;
    }
    free(nodo_a_eliminar);
    return pagina;
}

void inicializar_sistema() {
    int memoria_fisica_mb;
    printf("Ingrese el tamaño de la memoria física (MB): ");
    scanf("%d", &memoria_fisica_mb);

    printf("Ingrese el tamaño de cada página (KB): ");
    scanf("%d", &tamaño_pagina_kb);

    memoria_fisica_kb = memoria_fisica_mb * 1024;

    srand(time(NULL));
    float factor = ((float)(rand() % 31 + 15)) / 10; 
    memoria_virtual_kb = (int)(memoria_fisica_kb * factor);

    printf("Memoria virtual asignada: %d KB\n", memoria_virtual_kb);

    marcos_totales_ram = memoria_fisica_kb / tamaño_pagina_kb;
    marcos_totales_swap = memoria_virtual_kb / tamaño_pagina_kb - marcos_totales_ram;

    printf("Marcos totales en RAM: %d\n", marcos_totales_ram);
    printf("Marcos totales en Swap: %d\n", marcos_totales_swap);

    marcos_ram = (Pagina **)malloc(sizeof(Pagina *) * marcos_totales_ram);
    marcos_swap = (Pagina **)malloc(sizeof(Pagina *) * marcos_totales_swap);

    for (int i = 0; i < marcos_totales_ram; i++) {
        marcos_ram[i] = NULL;
    }
    for (int i = 0; i < marcos_totales_swap; i++) {
        marcos_swap[i] = NULL;
    }
}

void crear_proceso() {
    Proceso *nuevo_proceso = (Proceso *)malloc(sizeof(Proceso));
    nuevo_proceso->id_proceso = id_proceso_actual++;
    nuevo_proceso->tamaño = rand() % (20000 - 1000 + 1) + 1000; 
    nuevo_proceso->num_paginas = nuevo_proceso->tamaño / tamaño_pagina_kb;
    if (nuevo_proceso->tamaño % tamaño_pagina_kb != 0) {
        nuevo_proceso->num_paginas++;
    }
    nuevo_proceso->tabla_paginas = NULL;
    nuevo_proceso->siguiente = NULL;

    printf("Creando proceso %d de tamaño %d KB (%d páginas)\n", nuevo_proceso->id_proceso, nuevo_proceso->tamaño, nuevo_proceso->num_paginas);

    for (int i = 0; i < nuevo_proceso->num_paginas; i++) {
        Pagina *nueva_pagina = (Pagina *)malloc(sizeof(Pagina));
        nueva_pagina->id_proceso = nuevo_proceso->id_proceso;
        nueva_pagina->num_pagina = i;
        nueva_pagina->num_marco = -1;
        nueva_pagina->presencia = FALSE;
        nueva_pagina->siguiente = NULL;

        if (marcos_ocupados_ram < marcos_totales_ram) {
            int marco_libre = -1;
            for (int j = 0; j < marcos_totales_ram; j++) {
                if (marcos_ram[j] == NULL) {
                    marco_libre = j;
                    break;
                }
            }
            if (marco_libre != -1) {
                marcos_ram[marco_libre] = nueva_pagina;
                nueva_pagina->num_marco = marco_libre;
                nueva_pagina->presencia = TRUE;
                marcos_ocupados_ram++;
                encolar_pagina_ram(nueva_pagina);
            }
        } else {
            if (marcos_ocupados_swap < marcos_totales_swap) {
                int marco_swap_libre = -1;
                for (int j = 0; j < marcos_totales_swap; j++) {
                    if (marcos_swap[j] == NULL) {
                        marco_swap_libre = j;
                        break;
                    }
                }
                if (marco_swap_libre != -1) {
                    marcos_swap[marco_swap_libre] = nueva_pagina;
                    nueva_pagina->num_marco = marco_swap_libre;
                    nueva_pagina->presencia = FALSE;
                    marcos_ocupados_swap++;
                } else {
                    printf("No hay espacio en Swap. Terminando simulación.\n");
                    exit(0);
                }
            } else {
                printf("No hay espacio en Swap. Terminando simulación.\n");
                exit(0);
            }
        }

        nueva_pagina->siguiente = nuevo_proceso->tabla_paginas;
        nuevo_proceso->tabla_paginas = nueva_pagina;
    }

    nuevo_proceso->siguiente = lista_procesos;
    lista_procesos = nuevo_proceso;
}

void finalizar_proceso() {
    if (lista_procesos == NULL) {
        return;
    }

    int count = 0;
    Proceso *temp = lista_procesos;
    while (temp != NULL) {
        count++;
        temp = temp->siguiente;
    }

    int indice = rand() % count;
    Proceso *proceso_actual = lista_procesos;
    Proceso *proceso_anterior = NULL;

    for (int i = 0; i < indice; i++) {
        proceso_anterior = proceso_actual;
        proceso_actual = proceso_actual->siguiente;
    }

    printf("Finalizando proceso %d\n", proceso_actual->id_proceso);

    Pagina *pagina_actual = proceso_actual->tabla_paginas;
    while (pagina_actual != NULL) {
        Pagina *pagina_a_eliminar = pagina_actual;
        pagina_actual = pagina_actual->siguiente;

        if (pagina_a_eliminar->presencia == TRUE) {
            marcos_ram[pagina_a_eliminar->num_marco] = NULL;
            marcos_ocupados_ram--;
            NodoCola *nodo_actual = frente_ram;
            NodoCola *nodo_anterior = NULL;
            while (nodo_actual != NULL) {
                if (nodo_actual->pagina == pagina_a_eliminar) {
                    if (nodo_anterior == NULL) {
                        frente_ram = nodo_actual->siguiente;
                    } else {
                        nodo_anterior->siguiente = nodo_actual->siguiente;
                    }
                    if (nodo_actual == final_ram) {
                        final_ram = nodo_anterior;
                    }
                    free(nodo_actual);
                    break;
                }
                nodo_anterior = nodo_actual;
                nodo_actual = nodo_actual->siguiente;
            }
        } else {
            marcos_swap[pagina_a_eliminar->num_marco] = NULL;
            marcos_ocupados_swap--;
        }

        free(pagina_a_eliminar);
    }

    if (proceso_anterior == NULL) {
        lista_procesos = proceso_actual->siguiente;
    } else {
        proceso_anterior->siguiente = proceso_actual->siguiente;
    }

    free(proceso_actual);
}

void acceder_direccion_virtual() {
    if (lista_procesos == NULL) {
        return;
    }

    int count = 0;
    Proceso *temp = lista_procesos;
    while (temp != NULL) {
        count++;
        temp = temp->siguiente;
    }

    int indice = rand() % count;
    Proceso *proceso_actual = lista_procesos;
    for (int i = 0; i < indice; i++) {
        proceso_actual = proceso_actual->siguiente;
    }

    int direccion_virtual = rand() % proceso_actual->tamaño;
    int num_pagina = direccion_virtual / tamaño_pagina_kb;
    int desplazamiento = direccion_virtual % tamaño_pagina_kb;

    printf("Accediendo a dirección virtual %d del proceso %d (Página %d, Desplazamiento %d)\n", direccion_virtual, proceso_actual->id_proceso, num_pagina, desplazamiento);

    Pagina *pagina_actual = proceso_actual->tabla_paginas;
    while (pagina_actual != NULL) {
        if (pagina_actual->num_pagina == num_pagina) {
            break;
        }
        pagina_actual = pagina_actual->siguiente;
    }

    if (pagina_actual == NULL) {
        printf("Error: Página no encontrada en la tabla de páginas del proceso.\n");
        return;
    }

    if (pagina_actual->presencia == TRUE) {
        printf("La página %d está en RAM (Marco %d). Acceso exitoso.\n", num_pagina, pagina_actual->num_marco);
    } else {
        printf("Page Fault: La página %d no está en RAM. Realizando swapping...\n", num_pagina);

        if (marcos_ocupados_ram < marcos_totales_ram) {
            int marco_libre = -1;
            for (int i = 0; i < marcos_totales_ram; i++) {
                if (marcos_ram[i] == NULL) {
                    marco_libre = i;
                    break;
                }
            }
            if (marco_libre != -1) {
                marcos_ram[marco_libre] = pagina_actual;
                pagina_actual->num_marco = marco_libre;
                pagina_actual->presencia = TRUE;
                marcos_ocupados_ram++;
                encolar_pagina_ram(pagina_actual);
                marcos_swap[pagina_actual->num_marco] = NULL;
                marcos_ocupados_swap--;
                printf("La página %d se ha cargado en el marco %d de la RAM.\n", num_pagina, marco_libre);
            } else {
                printf("Error: No se encontró marco libre en RAM.\n");
                exit(0);
            }
        } else {
            Pagina *pagina_a_reemplazar = desencolar_pagina_ram();
            if (pagina_a_reemplazar != NULL) {
                int marco_swap_libre = -1;
                for (int i = 0; i < marcos_totales_swap; i++) {
                    if (marcos_swap[i] == NULL) {
                        marco_swap_libre = i;
                        break;
                    }
                }
                if (marco_swap_libre != -1) {
                    marcos_swap[marco_swap_libre] = pagina_a_reemplazar;
                    pagina_a_reemplazar->presencia = FALSE;
                    int marco_viejo = pagina_a_reemplazar->num_marco;
                    pagina_a_reemplazar->num_marco = marco_swap_libre;
                    marcos_ocupados_swap++;
                    marcos_ram[marco_viejo] = pagina_actual;
                    pagina_actual->num_marco = marco_viejo;
                    pagina_actual->presencia = TRUE;
                    encolar_pagina_ram(pagina_actual);
                    printf("Se reemplazó la página %d del proceso %d por la página %d del proceso %d en el marco %d.\n",
                           pagina_a_reemplazar->num_pagina, pagina_a_reemplazar->id_proceso,
                           pagina_actual->num_pagina, pagina_actual->id_proceso, marco_viejo);
                } else {
                    printf("No hay espacio en Swap. Terminando simulación.\n");
                    exit(0);
                }
            } else {
                printf("Error: No se pudo realizar el reemplazo de página.\n");
                exit(0);
            }
        }
    }
}

int main() {
    inicializar_sistema();

    int contador_creacion_procesos = 0;
    int contador_eventos = 0;

    while (TRUE) {
        sleep(1);
        tiempo_ejecucion++;

        if (tiempo_ejecucion % 2 == 0) {
            crear_proceso();
            contador_creacion_procesos = 0;
        }

        if (tiempo_ejecucion >= 30 && tiempo_ejecucion % 5 == 0) {
            finalizar_proceso();
            acceder_direccion_virtual();
            contador_eventos = 0;
        }
        if (marcos_ocupados_ram >= marcos_totales_ram && marcos_ocupados_swap >= marcos_totales_swap) {
            printf("No hay memoria disponible en RAM ni en Swap. Terminando simulación.\n");
            break;
        }
    }

    return 0;
}
