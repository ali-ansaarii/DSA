#include "InsertionSort.hpp"

using namespace std;

void insertionSort(vector<long long>& values) {
    for (size_t i = 1; i < values.size(); ++i) {
        const long long key = values[i];
        size_t j = i;

        while (j > 0 && values[j - 1] > key) {
            values[j] = values[j - 1];
            --j;
        }

        values[j] = key;
    }
}
