#include "../HPP/inode.hpp"
#include <algorithm>
using namespace std;

Inode::Inode(uint32_t _id,
             const string& _name,
             bool _isDir,
             mode_t _perms,
             size_t _size,
             Inode* _parent)
    : id(_id),
      name(_name),
      isDir(_isDir),
      perms(_perms),
      size(_size),
      ctime(time(nullptr)),
      mtime(ctime),
      parent(_parent) {}

Inode* Inode::findChild(const string& nombre) const {
    for (auto* h : children)
        if (h->name == nombre) return h;
    return nullptr;
}

bool Inode::addChild(Inode* hijo) {
    if (!isDir || findChild(hijo->name)) return false;
    children.push_back(hijo);
    hijo->parent = this;
    mtime = time(nullptr);
    return true;
}

bool Inode::removeChild(const string& nombre) {
    auto it = remove_if(children.begin(), children.end(),
                        [&](Inode* n) { return n->name == nombre; });
    if (it == children.end()) return false;
    children.erase(it, children.end());
    mtime = time(nullptr);
    return true;
}