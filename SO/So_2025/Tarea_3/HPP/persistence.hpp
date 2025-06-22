#pragma once

class FsTree;  

namespace persistence {
    void save(const FsTree& fs);
    void load(FsTree& fs);
}
