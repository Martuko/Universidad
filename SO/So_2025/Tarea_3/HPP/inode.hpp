#pragma once
#include <string>
#include <vector>
#include <ctime>
#include <cstdint>

struct Inode {
    uint32_t            id;
    std::string         name;
    bool                isDir;
    mode_t              perms;   // rwx: usa sólo los bits de usuario
    size_t              size;    // 0 si directorio
    time_t              ctime;
    time_t              mtime;
    Inode*              parent;
    std::vector<Inode*> children;

    Inode(uint32_t _id,
          const std::string& _name,
          bool _isDir,
          mode_t _perms,
          size_t _size = 0,
          Inode* _parent = nullptr);

    Inode*  findChild(const std::string& nombre) const;
    bool    addChild(Inode* hijo);
    bool    removeChild(const std::string& nombre);
};
