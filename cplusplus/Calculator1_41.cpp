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

/*
#include <iomanip>
std::cout << std::fixed << std::setprecision(2) << num;
*/

#include <iostream>
// #include <cmath>
// #include <string>
#include <iomanip>
// using namespace std;

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8
    system("chcp 65001");

    std::cout << "Calculator App" << std::endl;

    double num1 = 0;
    double num2 = 1;
    std::cin >> num1;
    std::cin >> num2;
    // std::cout << "First number: " << num1 << std::endl;
    // std::cout << "Second number: " << num2 << std::endl;
    std::cout << std::fixed << std::setprecision(2) << "Sum: " << num1 + num2 << std::endl;
    std::cout << "Difference: " << num1 - num2 << std::endl;                 // 這裡的 Difference 也會是固定點兩位小數
    std::cout << "Product: " << num1 * num2 << std::endl;                    // 這裡的 Product 也會是固定點兩位小數
    std::cout << "Division: " << (num2 != 0 ? num1 / num2 : 0) << std::endl; // 這裡的 Division 也會是固定點兩位小數

    system("pause"); // 按任意鍵結束
    return 0;
}