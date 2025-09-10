// Nested Loops

/*

*/

/*

*/

#include <iostream>
// #include <cmath>
// #include <string>
// #include <iomanip>
// using namespace std;

int sigma(int n)
{
    // Write your code below
    // int sum = 0;
    // for (int i = 0; i < n; i++)
    // {
    //     sum += i;
    // }
    // return sum;
    if (n < 0)
        return 0;
    // 對於負數，總和定義為 0 是合理的。

    return n * (n + 1) / 2;
}

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    system("chcp 65001");

    int n;
    std::cin >> n;
    int res = sigma(n);
    std::cout << res;

    system("pause"); // 按任意鍵結束
    return 0;
}
