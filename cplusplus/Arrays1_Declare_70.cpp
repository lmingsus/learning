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

#include <iostream>
// #include <cmath>
// #include <string> // getline
// #include <iomanip>
// using namespace std;
// #include <clocale>

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    // system("chcp 65001");

    int numbers[5];
    int len = std::size(numbers); // C++17
    std::cout << "std::size(numbers) = " << len << std::endl;
    for (int i = 0; i < 5; i++)
    {
        std::cout << numbers[i] << " ";
    }
    std::cout << std::endl;

    // Create the shoppingList array here
    std::string shoppingList[] = {"bread", "eggs", "milk", "butter"};

    // Don't change the code below
    std::cout << "Shopping List:" << std::endl;
    for (int i = 0; i < std::size(shoppingList); i++)
    {
        std::cout << shoppingList[i] << std::endl;
    }

    system("pause"); // 按任意鍵結束
    return 0;
}
