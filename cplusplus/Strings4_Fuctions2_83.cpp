// String Operations

/*
std::string str = "Hello, World!";

str.insert(5, " C++");
Output: "Hello C++, World!"

str.replace(7, 5, "C++");
Output: "Hello, C++!"

str.substr(0, 5);
Output: "Hello"

str.substr(7, 5);
Output: "World"

str.substr(7);
Output: "World!"

str.append(" This is C++");
Output: "Hello, World! This is C++"
*/

/*
std::string str = "Hello, World!";

int pos = str.find("World");
Output: pos = 7 (position where "World" starts)
如果找不到，find() 回傳 std::string::npos。

str.erase(5, 2);
Output: "Hello World!"

str.clear();
Output: "" (empty string)

bool isEmpty = str.empty();
Returns true if str has no characters
*/

/*
std::string::find() 函式的回傳類型是 std::string::size_type
size_type 是一種無號整數（unsigned integer），這意味著它不能是負數。

一個 N 位元的無號整數可以表示的數字範圍是從 0 到 2^N - 1
64 位元無號整數的最大值是 2^64 - 1，即 18446744073709551615。

std::string::npos
C++ 標準庫定義了一個特殊的靜態常數 std::string::npos（"no position" 的縮寫）。
這個常數被定義為 size_type 所能表示的最大值。
*/

#include <iostream>
// #include <cmath>
#include <string> // getline
// #include <iomanip>
// #include <clocale>
// #include <cstring> // 使用 strlen()
// using namespace std;

void stringSearchOperations(std::string str)
{
    // Find first space
    std::cout << "Space Found At: " << str.find(" ") << std::endl;
    // Erase 4 characters from position 5
    std::cout << "After Erase: " << str.erase(5, 4) << std::endl;
    // Check if contains "You"
    bool found = (str.find("You") != std::string::npos);
    std::cout << "Contains You: " << (found ? "Found" : "Not Found") << std::endl;
    // Clear string and check if empty
    str.clear();
    std::cout << "Is Empty: " << str.empty() << std::endl;
}

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    // system("chcp 65001 >> nul");

    // std::boolalpha 讓布林值以 "true" 或 "false" 的形式輸出，而不是 1 或 0
    std::cout << std::boolalpha;

    std::string str;
    std::getline(std::cin, str);
    stringSearchOperations(str);

    system("pause"); // 按任意鍵結束
    return 0;
}
