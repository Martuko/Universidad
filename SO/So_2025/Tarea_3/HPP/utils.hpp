#pragma once
#include <string>
#include <sys/stat.h>

namespace utils {
    std::string permsToStr(mode_t p);
}
