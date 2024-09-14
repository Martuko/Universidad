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

using namespace std;

int main(int argc, char const *argv[])
{
    cout<<"El jugador de pid: "<<getpid()<<" se amurra y retira del juego "<<endl;

    pid_t pid= getpid();

    kill(pid,SIGTERM);

    exit(0);

    return 0;
}