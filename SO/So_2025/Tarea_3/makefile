CXX      = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

SRC := $(wildcard CPP/*.cpp)
SRC := $(shell find . -name '*.cpp')
OBJ := $(SRC:.cpp=.o)

myfs: $(OBJ)
	$(CXX) $^ -o $@

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) myfs .myfs.img .myfs_history