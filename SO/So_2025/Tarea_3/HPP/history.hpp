#pragma once
#include <vector>
#include <string>

class History {
public:
    void load();
    void save() const;
    void add(const std::string& line);
    void show() const;
    bool get(size_t idx, std::string& out) const;

private:
    std::vector<std::string> hist;
};