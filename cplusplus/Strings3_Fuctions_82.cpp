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

#include <iostream>
// #include <cmath>
#include <string> // getline
// #include <iomanip>
// #include <clocale>
// #include <cstring> // 使用 strlen()
// using namespace std;

void stringOperations(std::string str)
{
    // 1. Print length of the string
    std::cout << "Length: " << str.length() << std::endl;
    // 2. Append " - Modified" to the string
    str.append(" - Modified");
    std::cout << "Append: " << str << std::endl;

    // 3. Insert "C++ " at the beginning
    str.insert(0, "C++ ");
    std::cout << "Insert: " << str << std::endl;

    // 4. Extract substring of length 5 starting at position 5
    std::cout << "Extract: " << str.substr(5, 5) << std::endl;

    // 5. Replace substring of length 5 at position 5 with "Awesome"
    str.replace(5, 5, "Awesome");
    std::cout << "Replace: " << str << std::endl;
}
int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    // system("chcp 65001 >> nul");

    std::string str;
    std::getline(std::cin, str);
    stringOperations(str);

    system("pause"); // 按任意鍵結束
    return 0;
}
