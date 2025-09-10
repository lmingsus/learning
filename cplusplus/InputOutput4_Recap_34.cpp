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

    // Till 120
    int year;
    std::cin >> year;
    std::cout << 120 - year << " years till 120" << std::endl;
    // std::cout;

    // True or False
    // The program will output "T" if the input equals to “1” and "F" otherwise.
    std::string input = "";
    std::cin >> input;
    std::cout << (input == "1" ? "T" : "F") << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}