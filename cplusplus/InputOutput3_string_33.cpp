// String Input

/*
std::string str;
std::cin >> str;
*/

/*
std::string str;
std::getline(std::cin, str);
*/

/*
int n;
std::string str;
std::cin >> n;
std::cin.ignore();  // Clear the newline from input buffer
std::getline(cin, str);
*/

#include <iostream>
// #include <cmath>
#include <string>
using namespace std;

int main()
{
    // 在 cmd 上先執「 chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8
    system("chcp 65001");

    std::string name;
    int count;
    std::cout << "How many times to greet: ";
    std::cin >> count;
    std::cin.ignore(); // Clear the newline from input buffer
    std::cout << "Enter your name: ";
    std::getline(std::cin, name); // 需要 #include <string>

    for (int i = 0; i < count; ++i)
    {
        std::cout << "Hello, " << name << "!" << std::endl;
    }

    system("pause"); // 按任意鍵結束
    return 0;
}