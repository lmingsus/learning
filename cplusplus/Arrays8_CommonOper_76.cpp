// Declaring Arrays

/*
讓編譯器自動推斷大小：
int numbers[] = {1, 2, 3, 4, 5};

宣告一個未初始化的陣，陣列內容是未定義的垃圾值
int numbers[5];

宣告並使用初始化列表，未提供值的元素會被自動初始化為 0
int numbers[5] = {10, 20};

C++11 的列表初始化語法，將所有元素初始化為 0
int numbers[5] {0};

int length = std::size(numbers);
*/

/*
for-each loop:
int numbers[] = {1, 2, 3, 4, 5};
for (int number : numbers) {
    std::cout << number << std::endl;
}
*/

#include <iostream>
// #include <cmath>
// #include <string> // getline
// #include <iomanip>
// using namespace std;
// #include <clocale>

double *calculateStats(double arr[], int size)
{
    // Write your code here
    double sum = 0;
    double average = 0;
    double max = arr[0];
    double min = arr[0];

    for (int i = 0; i < size; ++i)
    {
        sum += arr[i];
        if (arr[i] > max)
            max = arr[i];
        if (arr[i] < min)
            min = arr[i];
    }
    average = sum / size;

    double *newArr = new double[4];
    newArr[0] = sum;
    newArr[1] = average;
    newArr[2] = max;
    newArr[3] = min;

    return newArr;
}

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    // system("chcp 65001");

    int numbers[] = {1, 2, 3, 4, 5};
    // 【情況一：傳值 (Pass-by-Value)】- for (auto item : container)
    for (int num : numbers)
    {
        num = 7; // 修改副本，不影響原始陣列
    }
    for (const int num : numbers)
    {
        std::cout << num << " "; // 1, 2, 3, 4, 5
    }
    std::cout << std::endl;

    // 【情況二：傳參考 (Pass-by-Reference)】- for (auto& item : container)
    // 當目的就是要修改容器內的元素時。
    for (int &num : numbers)
    {
        num = 7; // 修改原始陣列
    }
    for (const int num : numbers)
    {
        std::cout << num << " "; // 7, 7, 7, 7, 7
    }
    std::cout << std::endl;

    // 【情況三：傳常數參考 (Pass-by-Const-Reference)】 - for (const auto& item : container)
    // 當只需要讀取容器內容，且希望獲得最佳效能（避免複製）時。
    // 這是最常用、最推薦的唯讀遍歷方式。
    for (const int &num : numbers)
    {
        // num = 99; // 如果取消這一行的註解，程式將會編譯失敗！
        // 錯誤訊息：error: assignment of read-only reference 'num'
        std::cout << num << " "; // 7, 7, 7, 7, 7
    }
    std::cout << std::endl;

    int n;

    std::cin >> n;
    std::cin.ignore();
    double arr[n];

    for (int i = 0; i < n; i++)
    {
        double val;
        std::cin >> val;
        arr[i] = val;
    }

    double *stats = calculateStats(arr, n);
    std::cout << "Sum: " << stats[0] << std::endl;
    std::cout << "Average: " << stats[1] << std::endl;
    std::cout << "Maximum: " << stats[2] << std::endl;
    std::cout << "Minimum: " << stats[3] << std::endl;
    delete[] stats;

    system("pause"); // 按任意鍵結束
    return 0;
}
