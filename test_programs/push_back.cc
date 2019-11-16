#include <vector>
#include <string>

int main(int argc, char** argv) {
    int size = 10;
    if (argc > 1) {
        size = std::stoi(argv[1]);
    }

    std::vector<int> v;
    for (int i = 0; i < size; ++i)
        v.push_back(i);
}