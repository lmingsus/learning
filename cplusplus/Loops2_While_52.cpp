// For Loop Part 1

#include <iostream>
// #include <cmath>
// #include <string>
// #include <iomanip>
// using namespace std;

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    system("chcp 65001");

    double input = 0;
    std::cin >> input;
    while (input >= 3.5)
    {
        input /= 2;
    }
    std::cout << input << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}