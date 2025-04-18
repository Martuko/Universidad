#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <string.h>
#include <time.h>

#define MAX_TASKS 100
#define MAX_PROCESSES 6

typedef struct {
    int id;
    int arrival;
    int burst;
    pid_t sender_pid;
} Task;

Task tasks[MAX_TASKS];
int task_count = 0;

void execute_fcfs() {
    int current_time = 0;
    for (int i = 0; i < task_count - 1; i++) {
        for (int j = i + 1; j < task_count; j++) {
            if (tasks[i].arrival > tasks[j].arrival) {
                // Intercambiar tareas
                Task temp = tasks[i];
                tasks[i] = tasks[j];
                tasks[j] = temp;
            }
        }
    }

    for (int i = 0; i < task_count; i++) {
        if (tasks[i].arrival > current_time) {
            current_time = tasks[i].arrival;
        }
        int start_time = current_time;
        current_time += tasks[i].burst;
        int turnaround = current_time - tasks[i].arrival;
        printf("[PID %d] ID: %d | Llegada: %d | Fin: %d | Turnaround: %d\n",
               tasks[i].sender_pid, tasks[i].id, tasks[i].arrival, current_time, turnaround);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <N_procesos>\n", argv[0]);
        return 1;
    }

    int N = atoi(argv[1]);
    if (N < 2 || N > 6) {
        fprintf(stderr, "El número de procesos debe estar entre 2 y 6.\n");
        return 1;
    }

    char fifo_name[64];
    Task temp;

    srand(time(NULL));

    for (int i = 0; i < N; i++) {
        snprintf(fifo_name, sizeof(fifo_name), "/tmp/pipe_proceso%d", i);
        mkfifo(fifo_name, 0666);
    }

    for (int i = 0; i < N; i++) {
        snprintf(fifo_name, sizeof(fifo_name), "/tmp/pipe_proceso%d", i);
        int fd = open(fifo_name, O_RDONLY);
        while (read(fd, &temp, sizeof(Task)) > 0) {
            tasks[task_count++] = temp;
        }
        close(fd);
    }
    execute_fcfs();
    return 0;
}
