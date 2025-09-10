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

    for (int i = 3; i <= 27; i++)
    {
        std::cout << "Hello Coddy: " << i << std::endl;
    }

    system("pause"); // 按任意鍵結束
    return 0;
}