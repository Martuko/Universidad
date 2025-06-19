#include "../HPP/persistencia.hpp"
#include <fstream>
#include <unordered_map>
using namespace std;

/* formato: ver guía previa (cabecera + tupla por inode) */
namespace {
    constexpr uint32_t MAGIC = 0x4D465331; // "MFS1"
}

namespace persistence {

void saveNode(ofstream& out, Inode* n) {
    uint16_t nameLen = n->name.size();
    uint8_t flags = n->isDir ? 1 : 0;
    out.write(reinterpret_cast<char*>(&n->id), 4);
    uint32_t pid = n->parent ? n->parent->id : 0;
    out.write(reinterpret_cast<char*>(&pid), 4);
    out.write(reinterpret_cast<char*>(&flags), 1);
    out.write(reinterpret_cast<char*>(&n->perms), 1);
    out.write(reinterpret_cast<char*>(&n->size), 8);
    out.write(reinterpret_cast<char*>(&n->ctime), 8);
    out.write(reinterpret_cast<char*>(&n->mtime), 8);
    out.write(reinterpret_cast<char*>(&nameLen), 2);
    out.write(n->name.data(), nameLen);
    for (auto* h : n->children) saveNode(out, h);
}

void walkCount(Inode* n, uint32_t& c) {
    ++c;
    for (auto* h : n->children) walkCount(h, c);
}

void save(const FsTree& fs) {
    ofstream out(".myfs.img", ios::binary | ios::trunc);
    uint32_t count = 0; walkCount(fs.resolvePath("/"), count);
    out.write(reinterpret_cast<char const*>(&MAGIC), 4);
    out.write(reinterpret_cast<char const*>(&count), 4);
    saveNode(out, fs.resolvePath("/"));
}

void load(FsTree& fs) {
    ifstream in(".myfs.img", ios::binary);
    if (!in) return; // primera vez
    uint32_t magic, count;
    in.read(reinterpret_cast<char*>(&magic), 4);
    if (magic != MAGIC) return;
    in.read(reinterpret_cast<char*>(&count), 4);

    unordered_map<uint32_t, Inode*> map;
    fs.~FsTree(); new(&fs) FsTree(); // reset
    for (uint32_t i = 0; i < count; ++i) {
        uint32_t id, pid; uint8_t flags, perms; uint64_t size;
        int64_t ct, mt; uint16_t len;
        in.read(reinterpret_cast<char*>(&id), 4);
        in.read(reinterpret_cast<char*>(&pid), 4);
        in.read(reinterpret_cast<char*>(&flags), 1);
        in.read(reinterpret_cast<char*>(&perms), 1);
        in.read(reinterpret_cast<char*>(&size), 8);
        in.read(reinterpret_cast<char*>(&ct), 8);
        in.read(reinterpret_cast<char*>(&mt), 8);
        in.read(reinterpret_cast<char*>(&len), 2);
        string name(len, '\0');
        in.read(name.data(), len);

        auto* node = new Inode(id, name, flags & 1, perms, size);
        node->ctime = ct; node->mtime = mt;
        map[id] = node;
        if (pid == 0) continue;              // root
        map[pid]->addChild(node);
    }
}
} // namespace persistence
