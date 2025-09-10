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

    int n;
    std::cin >> n;
    // Write your code below
    for (int i = 1; i < n; i++)
    {
        std::cout << i << " " << n - i << std::endl;
    }

    system("pause"); // 按任意鍵結束
    return 0;
}