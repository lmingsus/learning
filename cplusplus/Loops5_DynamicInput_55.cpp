// Nested Loops

#include <iostream>
// #include <cmath>
// #include <string>
// #include <iomanip>
// using namespace std;

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    system("chcp 65001");

    int count = 0;
    double sum = 0;
    double add = 0;
    std::cin >> count;
    for (int i = 0; i < count; i++)
    {
        std::cin >> add;
        sum += add;
    }
    std::cout << sum << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}