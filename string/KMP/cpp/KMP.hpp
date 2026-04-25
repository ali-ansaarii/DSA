#pragma once

#include <string>
#include <vector>

using namespace std;

vector<int> buildLPS(const string& pattern);
vector<int> KMP(const string& text, const string& pattern);
