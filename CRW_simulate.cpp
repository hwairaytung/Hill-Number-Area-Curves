#include <cmath>
#include <cstdint>
#include <ctime>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

using namespace std;

static random_device rd;
static mt19937_64 rng(rd());

long long pair_xy(int x, int y) {
    long long xx = (x >= 0) ? 2LL * x : -2LL * x - 1LL;
    long long yy = (y >= 0) ? 2LL * y : -2LL * y - 1LL;
    long long s = xx + yy;
    return (s * (s + 1)) / 2 + yy;
}

pair<int, int> unpair_z(long long z) {
    long long w = static_cast<long long>(floor((sqrt(8.0 * z + 1.0) - 1.0) / 2.0));
    long long t = (w * w + w) / 2;
    long long y = z - t;
    long long x = w - y;

    if (x % 2 == 0) {
        x = x / 2;
    } else {
        x = -(x + 1) / 2;
    }

    if (y % 2 == 0) {
        y = y / 2;
    } else {
        y = -(y + 1) / 2;
    }

    return pair<int, int>(static_cast<int>(x), static_cast<int>(y));
}

double rand01() {
    uniform_real_distribution<double> dist(0.0, 1.0);
    return dist(rng);
}

long long next_spot(long long current_spot) {
    pair<int, int> p = unpair_z(current_spot);
    int x = p.first;
    int y = p.second;
    double yay = rand01();

    if (yay < 0.25) {
        return pair_xy(x + 1, y);
    } else if (yay < 0.5) {
        return pair_xy(x - 1, y);
    } else if (yay < 0.75) {
        return pair_xy(x, y + 1);
    } else {
        return pair_xy(x, y - 1);
    }
}

string json_int_list(const vector<int>& v) {
    string s = "[";
    for (size_t i = 0; i < v.size(); ++i) {
        if (i > 0) {
            s += ",";
        }
        s += to_string(v[i]);
    }
    s += "]";
    return s;
}

string json_result(const vector<vector<int>>& result) {
    string s = "[";
    for (size_t i = 0; i < result.size(); ++i) {
        if (i > 0) {
            s += ",";
        }
        s += json_int_list(result[i]);
    }
    s += "]";
    return s;
}

int main() {
    const int L = 1600;
    const double max_r = 1;

    const int N = static_cast<int>(pow(L, max_r));
    const double alpha = 1.0 / (L * L);

    unordered_map<long long, vector<int> > current_walkers;
    current_walkers.reserve(static_cast<size_t>(N) * static_cast<size_t>(N) * 2);

    vector<long long> active_keys;
    active_keys.reserve(static_cast<size_t>(N) * static_cast<size_t>(N));

    unordered_map<long long, size_t> key_index;
    key_index.reserve(static_cast<size_t>(N) * static_cast<size_t>(N) * 2);

    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            long long spot = pair_xy(i, j);
            current_walkers[spot] = vector<int>(1, i * N + j);
            key_index[spot] = active_keys.size();
            active_keys.push_back(spot);
        }
    }

    vector<vector<int> > result;
    result.reserve(active_keys.size());

    while (current_walkers.size() > 1) {
        uniform_int_distribution<size_t> pick_dist(0, active_keys.size() - 1);
        long long walker = active_keys[pick_dist(rng)];

        if (rand01() < alpha / (1.0 + alpha)) {
            result.push_back(current_walkers[walker]);
            current_walkers.erase(walker);

            size_t idx = key_index[walker];
            long long last_key = active_keys.back();
            active_keys[idx] = last_key;
            key_index[last_key] = idx;
            active_keys.pop_back();
            key_index.erase(walker);

            cout << current_walkers.size() << '\n';
        } else {
            long long new_dest = next_spot(walker);

            unordered_map<long long, vector<int> >::iterator dest_it = current_walkers.find(new_dest);
            if (dest_it != current_walkers.end()) {
                dest_it->second.insert(
                    dest_it->second.end(),
                    current_walkers[walker].begin(),
                    current_walkers[walker].end()
                );
                current_walkers.erase(walker);

                size_t idx = key_index[walker];
                long long last_key = active_keys.back();
                active_keys[idx] = last_key;
                key_index[last_key] = idx;
                active_keys.pop_back();
                key_index.erase(walker);
            } else {
                current_walkers[new_dest] = current_walkers[walker];
                current_walkers.erase(walker);

                size_t idx = key_index[walker];
                active_keys[idx] = new_dest;
                key_index.erase(walker);
                key_index[new_dest] = idx;
            }
        }
    }

    if (current_walkers.size() == 1) {
        result.push_back(current_walkers.begin()->second);
    }

    time_t now_time = time(NULL);
    tm local_tm;

#ifdef _WIN32
    localtime_s(&local_tm, &now_time);
#else
    local_tm = *localtime(&now_time);
#endif

    ostringstream ts;
    ts << put_time(&local_tm, "%Y%m%d%H%M%S");

    string filename = "CRW_L" + to_string(L) + "_" + ts.str() + ".json";

    ofstream out(filename.c_str(), ios::binary);
    out << json_result(result);
    out.close();

    return 0;
}