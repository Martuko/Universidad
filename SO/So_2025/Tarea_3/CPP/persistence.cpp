#include "../HPP/tree.hpp"
#include "../HPP/persistence.hpp"
#include <fstream>
#include <unordered_map>
using namespace std;

namespace {
    constexpr uint32_t MAGIC = 0x4D465331;
}

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

namespace persistence {

void save(const FsTree& fs) {
    ofstream out(".myfs.img", ios::binary | ios::trunc);
    if (!out) return;

    uint32_t count = 0;
    Inode* root = fs.resolvePath("/");  
    walkCount(root, count);

    out.write(reinterpret_cast<const char*>(&MAGIC), 4);
    out.write(reinterpret_cast<const char*>(&count), 4);
    saveNode(out, root);
}

void load(FsTree& fs) {
    ifstream in(".myfs.img", ios::binary);
    if (!in) return;

    uint32_t magic, count;
    in.read(reinterpret_cast<char*>(&magic), 4);
    in.read(reinterpret_cast<char*>(&count), 4);
    if (magic != MAGIC || count == 0) return;

    unordered_map<uint32_t, Inode*> nodos;
    unordered_map<uint32_t, uint32_t> padres;
    Inode* nuevaRaiz = nullptr;
    uint32_t maxId = 0;

    for (uint32_t i = 0; i < count; ++i) {
        uint32_t id, pid;
        uint8_t flags, perms;
        uint64_t size;
        int64_t ctime, mtime;
        uint16_t len;

        in.read(reinterpret_cast<char*>(&id), 4);
        in.read(reinterpret_cast<char*>(&pid), 4);
        in.read(reinterpret_cast<char*>(&flags), 1);
        in.read(reinterpret_cast<char*>(&perms), 1);
        in.read(reinterpret_cast<char*>(&size), 8);
        in.read(reinterpret_cast<char*>(&ctime), 8);
        in.read(reinterpret_cast<char*>(&mtime), 8);
        in.read(reinterpret_cast<char*>(&len), 2);

        string name(len, '\0');
        in.read(&name[0], len);

        Inode* n = new Inode(id, name, flags & 1, perms, size);
        n->ctime = ctime;
        n->mtime = mtime;
        nodos[id] = n;
        padres[id] = pid;
        if (pid == 0) nuevaRaiz = n;
        maxId = max(maxId, id);
    }

    for (auto& [id, nodo] : nodos) {
        uint32_t pid = padres[id];
        if (pid != 0 && nodos.count(pid)) {
            nodos[pid]->addChild(nodo);
        }
    }

    if (!nuevaRaiz) return; 

    fs.clearRec(fs.root);         
    fs.root = nuevaRaiz;
    fs.cwd = nuevaRaiz;
    fs.nextId = maxId + 1;
}

} 
