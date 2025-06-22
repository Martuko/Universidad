#include "../HPP/tree.hpp"
#include "../HPP/persistence.hpp"
#include "../HPP/utils.hpp"
#include <iostream>
#include <iomanip>
#include <stack>
using namespace std;

FsTree::FsTree()
    : root(new Inode(1, "/", true, S_IRWXU)),
      cwd(root),
      nextId(2) {}

FsTree::~FsTree() { clearRec(root); }

void FsTree::clearRec(Inode* n) {
    for (auto* h : n->children) clearRec(h);
    delete n;
}

vector<string> FsTree::split(const string& path) {
    vector<string> parts;
    string token;
    for (size_t i = 0; i < path.size(); ++i) {
        if (path[i] == '/') {
            if (!token.empty()) { parts.push_back(token); token.clear(); }
        } else token.push_back(path[i]);
    }
    if (!token.empty()) parts.push_back(token);
    return parts;
}

Inode* FsTree::resolvePath(const string& path) const {
    Inode* cur = (path.empty() || path[0] != '/') ? cwd : root;
    for (const string& part : split(path)) {
        if (part == ".") continue;
        if (part == "..") {
            if (cur->parent) cur = cur->parent;
            continue;
        }
        cur = cur->findChild(part);
        if (!cur) return nullptr;
    }
    return cur;
}

string FsTree::cwdAbsPath() const {
    string result;
    stack<string> st;
    for (Inode* n = cwd; n; n = n->parent) st.push(n->name);
    while (!st.empty()) {
        string seg = st.top(); st.pop();
        if (seg != "/" && !result.empty()) result += "/";
        result += seg;
    }
    return result;
}

bool FsTree::mkdir(const string& path) {
    auto parts = split(path);
    string name = parts.back();
    parts.pop_back();
    /* padre */
    string parentPath = path[0] == '/' ? "/" : "";
    for (size_t i = 0; i < parts.size(); ++i) {
        parentPath += parts[i];
        if (i + 1 < parts.size()) parentPath += "/";
    }
    Inode* parent = resolvePath(parentPath);
    if (!parent || !parent->isDir) return false;
    if (!(parent->perms & S_IWUSR) || !(parent->perms & S_IXUSR)) return false;
    auto* nuevo = new Inode(nextId++, name, true, S_IRWXU);
    return parent->addChild(nuevo);
}

bool FsTree::touch(const string& path) {
    auto parts = split(path);
    string name = parts.back();
    parts.pop_back();
    string parentPath = path[0] == '/' ? "/" : "";
    for (size_t i = 0; i < parts.size(); ++i) {
        parentPath += parts[i];
        if (i + 1 < parts.size()) parentPath += "/";
    }
    Inode* parent = resolvePath(parentPath);
    if (!parent || !parent->isDir) return false;
    if (!(parent->perms & S_IWUSR)) return false;
    auto* nuevo = new Inode(nextId++, name, false, S_IRUSR | S_IWUSR);
    return parent->addChild(nuevo);
}

bool FsTree::rm(const string& path) {
    Inode* nodo = resolvePath(path);
    if (!nodo || nodo == root) return false;
    if (nodo->isDir && !nodo->children.empty()) return false;
    if (!(nodo->parent->perms & S_IWUSR)) return false;
    nodo->parent->removeChild(nodo->name);
    delete nodo;
    return true;
}

bool FsTree::mv(const string& oldPath, const string& newName) {
    Inode* n = resolvePath(oldPath);
    if (!n || n == root) return false;
    if (n->parent->findChild(newName)) return false;
    n->name = newName;
    n->parent->mtime = time(nullptr);
    return true;
}

bool FsTree::chmod(const string& path, mode_t add, mode_t sub) {
    Inode* n = resolvePath(path);
    if (!n) return false;
    n->perms |= add;
    n->perms &= ~sub;
    n->mtime = time(nullptr);
    return true;
}

bool FsTree::cd(const string& path) {
    Inode* n = resolvePath(path);
    if (!n || !n->isDir || !(n->perms & S_IXUSR)) return false;
    cwd = n;
    return true;
}

void FsTree::pwd() const { cout << cwdAbsPath() << '\n'; }

void FsTree::lsRec(Inode* dir, const string& prefix, bool showId, bool recursive) const {
    for (auto* h : dir->children) {
        cout << prefix;
        if (showId) cout << setw(4) << h->id << " ";
        cout << utils::permsToStr(h->perms)
             << (h->isDir ? 'd' : '-') << " " << h->name << '\n';

        if (recursive && h->isDir) {
            cout << "\n" << cwdAbsPath() << "/" << h->name << ":\n";
            lsRec(h, prefix + "  ", showId, recursive);
        }
    }
}


void FsTree::ls(bool showId, bool recursive) const {
    lsRec(cwd, "", showId, recursive);
}

void FsTree::findRec(Inode* dir,
                     const string& name,
                     const string& abs) const {
    if (dir->name == name) cout << abs << '\n';
    for (auto* h : dir->children)
        findRec(h, name, abs + "/" + h->name);
}

void FsTree::find(const string& name) const {
    findRec(cwd, name, cwdAbsPath());
}

void FsTree::save() const { persistence::save(*this); }
void FsTree::load()       { persistence::load(*this); }