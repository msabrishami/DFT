#include <array>
#include <bitset>
#include <cstdio>
#include <fstream>
#include <functional>
#include <iostream>
#include <math.h>
#include <memory>
#include <stdexcept>
#include <string>
#include <thread>
#include <time.h>
#include <vector>
using namespace std;

string exec(const string &cmd);

class ThreadPool {
public:
  // constructor
  ThreadPool(int _input_cnt, string _circuit_name, int _max_thread_cnt)
      : input_cnt(_input_cnt), circuit_name(_circuit_name),
        max_thread_cnt(_max_thread_cnt) {}
  void decide_thread_cnt() {
    if (input_cnt <= 3) {
      thread_cnt = 1;
    } else {
      thread_cnt = max_thread_cnt;
    }
    lines_per_thread = int(pow(2, input_cnt)) / thread_cnt;
  }

  void multithreading() {
    vector<thread> threads;
    for (int i = 0; i < thread_cnt; i++) {
      thread t(&ThreadPool::gen_fault_dic, this, i);
      // thread t([&]{ this->gen_fault_dic(i); });
      threads.push_back(std::move(t));
    }
    for (auto &t : threads) {
      t.join();
    }
  }
  void gen_fault_dic(int idx) {
    string res =
        exec("python3 parallel_processing.py " + circuit_name + " " + to_string(thread_cnt) + " " + to_string(idx));
    cout << res << endl;
  }

private:
  int input_cnt;
  int lines_per_thread;
  int thread_cnt;
  int max_thread_cnt;
  string circuit_name;
};

string exec(const string &cmd) {
  array<char, 128> buffer;
  string result;
  unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd.c_str(), "r"), pclose);
  if (!pipe) {
    throw runtime_error("popen() failed!");
  }
  while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
    result += buffer.data();
  }
  return result;
}



int main(int argc, char **argv) {
  string circuit_name;
  if (argc > 2) {
    cout << "Invalid Path Provided." << endl;
    exit(0);
  } else {
    circuit_name = argv[1];
    cout << circuit_name << endl;
  }
  string cnt =
      exec("python3 parallel_processing.py " + circuit_name + " -1 -1");
  
  int max_thread_cnt = thread::hardware_concurrency();
  // int max_thread_cnt = 2; // comment this line if you want the maximum thread operating at the same time
  int input_cnt = atoi(cnt.c_str());
  ThreadPool tp(input_cnt, circuit_name, max_thread_cnt);
  tp.decide_thread_cnt();
  tp.multithreading();
  return 0;
}