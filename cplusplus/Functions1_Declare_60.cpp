// Nested Loops

/*
access_modifier return_type method_name(parameters) {
    code
}
*/

#include <iostream>
// #include <cmath>
// #include <string>
// #include <iomanip>
// using namespace std;

// Method declaration
void sumNumbers()
{
    // Complete Method
    int sum = 0;
    for (int i = 1; i <= 1000; i++)
    {
        sum += i;
    }
    std::cout << sum << std::endl;
}

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    system("chcp 65001");

    int n;
    std::cin >> n;
    for (int i = 0; i < n; i++)
    {
        // Call the method n times
        sumNumbers();
    }

    system("pause"); // 按任意鍵結束
    return 0;
}
