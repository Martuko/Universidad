#include "../HPP/history.hpp"
#include <fstream>
#include <iostream>
using namespace std;

void History::load() {
    ifstream in(".myfs_history");
    string line;
    while (getline(in, line)) hist.push_back(line);
}

void History::save() const {
    ofstream out(".myfs_history", ios::trunc);
    for (auto const& l : hist) out << l << '\n';
}

void History::add(const string& l) { hist.push_back(l); }
void History::show() const {
    for (size_t i = 0; i < hist.size(); ++i)
        cout << i+1 << "  " << hist[i] << '\n';
}
bool History::get(size_t idx, string& out) const {
    if (idx == 0 || idx > hist.size()) return false;
    out = hist[idx-1]; return true;
}