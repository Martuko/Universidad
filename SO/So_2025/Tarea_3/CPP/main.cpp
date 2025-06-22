#include "../HPP/tree.hpp"
#include "../HPP/shell.hpp"
int main() {
    FsTree fs;
    fs.load();
    return mainShell(fs);  
    fs.save();              
    return 0;
}