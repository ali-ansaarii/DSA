#include "SelectionSort.hpp"

#include <utility>

using namespace std;

void selectionSort(vector<int>& values) {
    const int n = static_cast<int>(values.size());

    for (int i = 0; i < n; ++i) {
        int minIndex = i;
        for (int j = i + 1; j < n; ++j) {
            if (values[j] < values[minIndex]) {
                minIndex = j;
            }
        }

        if (minIndex != i) {
            swap(values[i], values[minIndex]);
        }
    }
}
