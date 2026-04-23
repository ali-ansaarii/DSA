#include "PreorderTraversal.hpp"

#include <chrono>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

static bool IsValidChildIndex(int child, int n) {
    return child == -1 || (child >= 0 && child < n);
}

int main(int argc, char* argv[]) {
    string inputPath = "../inputs/input.txt";
    bool timePreorder = false;

    for (int i = 1; i < argc; ++i) {
        const string arg = argv[i];
        if (arg == "--time-preorder") {
            timePreorder = true;
        } else {
            inputPath = arg;
        }
    }

    ifstream input(inputPath);
    if (!input) {
        cerr << "Failed to open input file: " << inputPath << '\n';
        return 1;
    }

    int n = 0;
    int root = -1;
    if (!(input >> n >> root) || n <= 0 || root < 0 || root >= n) {
        cerr << "Invalid tree header. Expected: n root" << '\n';
        return 1;
    }

    vector<int> leftChildren(n, -1);
    vector<int> rightChildren(n, -1);

    for (int node = 0; node < n; ++node) {
        int left = -1;
        int right = -1;
        if (!(input >> left >> right) || !IsValidChildIndex(left, n) || !IsValidChildIndex(right, n)) {
            cerr << "Invalid child pair at line " << (node + 2) << '\n';
            return 1;
        }

        leftChildren[node] = left;
        rightChildren[node] = right;
    }

    const auto traversalStart = chrono::steady_clock::now();
    const vector<int> order = PreorderTraversal(leftChildren, rightChildren, root);
    const auto traversalEnd = chrono::steady_clock::now();
    const auto traversalDuration =
        chrono::duration_cast<chrono::microseconds>(traversalEnd - traversalStart);

    if (timePreorder) {
        cout << "Visited nodes: " << order.size() << '\n';
        cout << "PreorderTraversal call time (ms): " << (traversalDuration.count() / 1000.0) << '\n';
    } else {
        cout << "Preorder traversal order:";
        for (const int node : order) {
            cout << ' ' << node;
        }
        cout << '\n';
    }

    return 0;
}
