/*
int age;
std::cout << "請輸入年齡：";
std::cin >> age;  // 會自動轉成 int
*/

/*
bool isAdult;
std::cout << "請輸入是否成年 (1 或 0)：";
輸入 0 會轉成 false，1 會轉成 true。
輸入 true 會轉成 true，輸入 false 會轉成 false。
*/

#include <iostream>
// #include <cmath>
// #include <string>
using namespace std;

int main()
{
    // 在 cmd 上先執「 chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8
    system("chcp 65001");

    int age;
    std::cout << "Enter your age: ";
    std::cin >> age;

    std::cout << "You are " << age << " years old." << std::endl;

    bool isAdult;
    std::cout << "你成年了嗎？(是：1 或 否：0)：";
    std::cin >> isAdult;
    std::cout << "你輸入的值是：" << isAdult;
    if (isAdult)
    {
        std::cout << "，你已經成年了。" << std::endl;
    }
    else
    {
        std::cout << "，你還未成年。" << std::endl;
    }

    system("pause"); // 按任意鍵結束
    return 0;
}