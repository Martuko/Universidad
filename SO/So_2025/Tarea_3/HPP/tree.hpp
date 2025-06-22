#pragma once
#include "inode.hpp"
#include <vector>
#include <string>

class FsTree;  


namespace persistence {
    void save(const FsTree&);
    void load(FsTree&);
}

class FsTree {
public:
    FsTree();
    ~FsTree();

    bool mkdir(const std::string& path);
    bool touch(const std::string& path);
    bool rm(const std::string& path);
    bool mv(const std::string& oldPath, const std::string& newName);
    bool chmod(const std::string& path, mode_t add, mode_t sub);
    bool cd(const std::string& path);
    void pwd() const;
    void ls(bool showId, bool recursive) const;
    void find(const std::string& name) const;

    void save() const;
    void load();

    friend void persistence::save(const FsTree&);
    friend void persistence::load(FsTree&);

private:
    Inode* root;
    Inode* cwd;
    uint32_t nextId;

    static std::vector<std::string> split(const std::string& path);
    Inode* resolvePath(const std::string& path) const;
    std::string cwdAbsPath() const;
    void lsRec(Inode* dir, const std::string& prefix, bool showId, bool recursive) const;
    void findRec(Inode*, const std::string&, const std::string&) const;
    void clearRec(Inode*);
};
