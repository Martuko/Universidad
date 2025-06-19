#pragma once
#include "tree.hpp"

namespace persistence {
    void save(const FsTree& fs);
    void load(FsTree& fs);
}
