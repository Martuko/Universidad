#include "../HPP/tree.hpp"
#include "../HPP/shell.hpp"
int main() {
    FsTree fs;
    fs.load();
    return mainShell(fs);   // forward-decl en shell/shell.cpp
}
