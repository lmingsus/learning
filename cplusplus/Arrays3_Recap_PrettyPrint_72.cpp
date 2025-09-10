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
Create a program that:

Receives n: the number of elements in the array
Then receives n strings to populate the array
Print the array beautifully in the following format:

[elem1, elem2, elem3, ...]
*/

#include <iostream>
// #include <cmath>
#include <string> // getline
// #include <iomanip>
// using namespace std;
// #include <clocale>

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    // system("chcp 65001");

    int n;

    std::cin >> n;
    std::cin.ignore();
    std::string arr[n];

    for (int i = 0; i < n; i++)
    {
        std::string val;
        std::cin >> val;
        arr[i] = val;
    }

    // Print the array beautifully
    std::cout << "[";
    // for (int i = 0; i < n; i++)
    // {
    //     std::cout << arr[i];
    //     if (i < n - 1)
    //     {
    //         std::cout << ", ";
    //     }
    // }
    const char *separator = ""; // 初始分隔符為空
    for (const auto &item : arr)
    {
        std::cout << separator << item;
        separator = ", "; // 從第二個元素開始，分隔符變為 ", "
    }
    std::cout << "]" << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}
