#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <time.h>
#include <string.h>

#define MAX_TASKS 6

typedef struct {
    int id;
    int arrival;
    int burst;
    pid_t sender_pid;
} Task;

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <ID_proceso>\n", argv[0]);
        return 1;
    }

    int process_id = atoi(argv[1]);
    if (process_id < 0 || process_id > 5) {
        fprintf(stderr, "El ID del proceso debe estar entre 0 y 5.\n");
        return 1;
    }

    char fifo_name[64];
    Task task;

    srand(time(NULL) + process_id);

    snprintf(fifo_name, sizeof(fifo_name), "/tmp/pipe_proceso%d", process_id);
    int fd = open(fifo_name, O_WRONLY);
    if (fd == -1) {
        perror("No se pudo abrir el pipe");
        return 1;
    }

    int task_count = rand() % 4 + 3;  
    for (int i = 0; i < task_count; i++) {
        task.id = i;
        task.arrival = rand() % 10;  
        task.burst = rand() % 5 + 1;  
        task.sender_pid = getpid();
        write(fd, &task, sizeof(Task));
    }

    close(fd);
    return 0;
}
