#include "../HPP/tree.hpp"  
#include "../HPP/history.hpp"  
#include <iostream>
#include <sstream>
#include <vector>
#include <sys/stat.h>

using namespace std;

static vector<string> tokenize(const string& line) {
    vector<string> res; istringstream iss(line); string t;
    while (iss >> t) res.push_back(t);
    return res;
}

int mainShell(FsTree& fs) {
    History history; history.load();
    string line;
    while (cout << "myfs> " && getline(cin, line)) {
        if (line.empty()) continue;
        history.add(line);
        auto tok = tokenize(line); string cmd = tok[0];

        if (cmd == "exit") break;
        if (cmd == "history") { history.show(); continue; }
        if (cmd[0] == '!' && cmd.size() > 1) { 
            size_t n = stoi(cmd.substr(1));
            string newCmd; if (history.get(n, newCmd)) {
                cout << newCmd << '\n';
                line = newCmd; tok = tokenize(line); cmd = tok[0];
            } else { cout << "Índice fuera de rango\n"; continue; }
        }

        if (cmd == "pwd") fs.pwd();
        else if (cmd == "cd" && tok.size() == 2) {
            if (!fs.cd(tok[1])) cout << "Error\n";
        }
        else if (cmd == "mkdir" && tok.size() == 2) {
            if (!fs.mkdir(tok[1])) cout << "Error\n";
        }
        else if (cmd == "touch" && tok.size() == 2) {
            if (!fs.touch(tok[1])) cout << "Error\n";
        }
        else if (cmd == "rm" && tok.size() == 2) {
            if (!fs.rm(tok[1])) cout << "Error\n";
        }
        else if (cmd == "mv" && tok.size() == 3) {
            if (!fs.mv(tok[1], tok[2])) cout << "Error\n";
        }
        else if (cmd == "chmod" && tok.size() >= 3) {
            mode_t add = 0, sub = 0;
            for (size_t i = 1; i + 1 < tok.size(); ++i) {
                const string& flag = tok[i];
                if (flag.empty()) continue;
                if (flag[0] == '+') {
                    for (char c : flag.substr(1)) {
                        if (c == 'r') add |= S_IRUSR;
                        else if (c == 'w') add |= S_IWUSR;
                        else if (c == 'x') add |= S_IXUSR;
                    }
                } else if (flag[0] == '-') {
                    for (char c : flag.substr(1)) {
                        if (c == 'r') sub |= S_IRUSR;
                        else if (c == 'w') sub |= S_IWUSR;
                        else if (c == 'x') sub |= S_IXUSR;
                    }
                }
            }
            const string& path = tok.back(); 
            if (!fs.chmod(path, add, sub)) cout << "Error\n";
        }
        
        else if (cmd == "ls") {
            bool id = false, rec = false;
            for (size_t i=1;i<tok.size();++i)
                if (tok[i]=="-i") id=true;
                else if (tok[i]=="-R") rec=true;
            fs.ls(id,rec);
        }
        else if (cmd == "find" && tok.size()==2) fs.find(tok[1]);
        else cout << "Comando no reconocido\n";
    }
    history.save(); fs.save();
    return 0;
}