// String Operations

/*
std::string str = "Hello";
str += " ";
str += "World";
std::cout << str;
Outputs: Hello World

int len = str.length();
int len = str.size();
std::cout << len; // Outputs: 5
*/

#include <iostream>
// #include <cmath>
#include <string> // getline
// #include <iomanip>
// #include <clocale>
// #include <cstring> // 使用 strlen()
// using namespace std;

std::string concatenateStrings(std::string str1, std::string str2)
{
    // Concatenate the strings and return the result
    return str1 + " " + str2;
}

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    // system("chcp 65001 >> nul");

    std::string pp = "Hello";
    pp.append(" World");
    std::cout << pp << std::endl;

    std::string firstName;
    std::string lastName;
    std::getline(std::cin, firstName);
    std::getline(std::cin, lastName);

    // Call concatenateStrings and store the result in fullName
    std::string fullName = concatenateStrings(firstName, lastName);

    // Print fullName
    std::cout << fullName;

    system("pause"); // 按任意鍵結束
    return 0;
}
