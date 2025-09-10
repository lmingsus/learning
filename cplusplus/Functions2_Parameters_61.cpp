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

// Function declaration
void product(int a, int b)
{
    std::cout << a * b << std::endl;
}

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    system("chcp 65001");

    int a, b;
    std::cin >> a >> b;
    // Call the function with a and b as arguments
    product(a, b);

    system("pause"); // 按任意鍵結束
    return 0;
}
