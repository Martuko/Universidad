#pragma once
#include "inode.hpp"
#include <string>
#include <vector>

class FsTree {
public:
    FsTree();
    ~FsTree();

    Inode*  resolvePath(const std::string& path) const;
    std::string cwdAbsPath() const;

    /* comandos */
    bool mkdir(const std::string& path);
    bool touch(const std::string& path);
    bool rm   (const std::string& path);
    bool mv   (const std::string& oldPath, const std::string& newName);
    bool chmod(const std::string& path, mode_t add, mode_t sub);
    bool cd   (const std::string& path);
    void pwd() const;
    void ls(bool showId, bool recursive) const;
    void find(const std::string& name) const;

    /* persistencia */
    void save() const;
    void load();

private:
    Inode*      root;
    Inode*      cwd;
    uint32_t    nextId;

    /* helpers internos */
    static std::vector<std::string> split(const std::string& path);
    void lsRec(Inode* dir,
               const std::string& prefix,
               bool showId) const;
    void findRec(Inode* dir,
                 const std::string& name,
                 const std::string& abs) const;
    void clearRec(Inode* n);
};
