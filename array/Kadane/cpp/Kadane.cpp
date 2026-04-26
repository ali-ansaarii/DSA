#include "Kadane.hpp"

#include <stdexcept>

using namespace std;

KadaneResult maxSubarrayKadane(const vector<long long>& values) {
    if (values.empty()) {
        throw invalid_argument("Kadane's Algorithm requires a non-empty array");
    }

    long long current_sum = values[0];
    long long best_sum = values[0];
    size_t current_start = 0;
    size_t best_start = 0;
    size_t best_end = 0;

    for (size_t i = 1; i < values.size(); ++i) {
        const long long extended_sum = current_sum + values[i];

        if (extended_sum < values[i]) {
            current_sum = values[i];
            current_start = i;
        } else {
            current_sum = extended_sum;
        }

        if (current_sum > best_sum) {
            best_sum = current_sum;
            best_start = current_start;
            best_end = i;
        }
    }

    return KadaneResult{best_sum, best_start, best_end};
}
