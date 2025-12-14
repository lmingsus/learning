// Pointer and Dynamic Array

/* C-style  動態陣列
建立一個動態陣列，會回傳一個指向該記憶體起始位置的指標 (pointer)。

int* numbers = new int[5];                // 未初始化，垃圾值
int* numbers = new int[5]();              // 零初始化，各元素初始化為 0
int* numbers = new int[5]{1, 5, 1, 9, 5}; // 使用列表初始化 (C++11)

new int[5] 的作用是在「堆積 (Heap)」上動態配置一塊能容納 5 個 int 的記憶體，
當使用 new[] 來手動配置記憶體時，就承擔了手動釋放這塊記憶體的責任。
這塊記憶體就會一直被佔用，直到程式結束，這就是所謂的「記憶體洩漏 (memory leak)」

delete[] numbers;  // 必須手動使用 delete[] 來釋放
*/

/*
C-style 靜態陣列
建立一個靜態陣列，會在「堆疊 (Stack)」上配置記憶體。

int numbers[5];            // 未初始化，垃圾值
int numbers[5] = {10, 20}; // 結果: {10, 20, 0, 0, 0}
int numbers[5] = {0};      // 傳統寫法
int numbers[5]{0};         // C++11 寫法，推薦
int numbers[] = {10, 20, 30}; // 編譯器會自動推斷大小為 3

沒有內建的大小資訊，傳遞給函式時會「退化」成指標，不安全。
*/

/*
std::array 是對 C-style 靜態陣列的現代化封裝

#include <array>

std::array<int, 5> numbers;                  // 未初始化
std::array<int, 5> numbers_zero{};           // 全部初始化為 0
std::array<int, 5> numbers_list = {10, 20}; // 結果: {10, 20, 0, 0, 0}

和 C-style 陣列一樣高效（在堆疊上），但它知道自己的大小 (.size())，固定大小陣列
支援邊界檢查 (.at())，
並且可以像其他物件一樣被複製和傳遞，不會退化成指標。
*/

/*
std::vector 是對 C-style 動態陣列的完美替代品。

#include <vector>

std::vector<int> numbers; // 建立一個空的 vector
numbers.push_back(10);    // 新增元素

建立一個包含 5 個元素的 vector，所有元素都初始化為 0
std::vector<int> numbers_sized(5);

使用列表初始化
std::vector<int> numbers_list = {1, 2, 3, 4, 5};

自動管理記憶體 (RAII)，完全不需要擔心 new 和 delete。
大小可以隨時改變，功能豐富，是你處理動態陣列時的首選。
*/

#include <iostream>
// #include <cmath>
// #include <string> // std::string, std::stoi, std::getline
// #include <iomanip> // For std::fixed and std::setprecision
// #include <clocale>
// #include <cstring> // 使用 strlen()
#include <vector>
#include <map>
// #include <set>
// #include <algorithm> // std::sort
// #include <stdexcept> // std::invalid_argument
// using namespace std;

int main()
{
    // Read the size of the array
    int size;
    std::cin >> size;

    // TODO: Write your code here
    // 1. Dynamically allocate an array using new[]
    int *arr = new int[size];
    // 2. Read the integers and store them in the array
    for (int i = 0; i < size; i++)
        std::cin >> arr[i];
    // 3. Calculate the sum of all numbers
    // 4. Find the maximum value
    int sum = 0;
    int max = arr[0];
    for (int i = 0; i < size; i++)
    {
        sum += arr[i];
        if (arr[i] > max)
            max = arr[i];
    }
    // 5. Don't forget to deallocate memory using delete[]
    delete[] arr;

    // Output the results (replace with actual variables)
    std::cout << "Array size: " << size << std::endl;
    std::cout << "Sum: " << sum << std::endl;
    std::cout << "Maximum: " << max << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}