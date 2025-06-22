#include "../HPP/utils.hpp"
using namespace std;

string utils::permsToStr(mode_t p) {
    string s;
    s += (p & S_IRUSR) ? 'r' : '-';
    s += (p & S_IWUSR) ? 'w' : '-';
    s += (p & S_IXUSR) ? 'x' : '-';
    return s;
}