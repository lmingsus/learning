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

Receives three inputs in this order:
n: the number of elements in the array
index: an index position (0 to n-1)
newElement: a new value (string)
Then receives n strings to populate the array
Modifies the array by replacing the element at index with the value newElement
Finally prints all elements of the modified array, one per line
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

    int n = 1;
    int index;
    std::string newElement;

    std::cin >> n;
    std::cin >> index;
    std::cin.ignore();
    std::getline(std::cin, newElement);
    std::string arr[n];

    for (int i = 0; i < n; i++)
    {
        std::getline(std::cin, arr[i]);
    }

    arr[index] = newElement;

    for (const auto &item : arr)
    {
        std::cout << item << std::endl;
    }

    system("pause"); // 按任意鍵結束
    return 0;
}
