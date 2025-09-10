// Do While Loop

#include <iostream>
// #include <cmath>
// #include <string>
// #include <iomanip>
// using namespace std;

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    system("chcp 65001");

    // Initialize variables
    int sum = 0;
    int number = 1;

    // Your code here
    do
    {
        sum += number;
        number += 2;
        std::cout << "Sum is: " << sum << std::endl;
        std::cout << "Num is: " << number << std::endl;
    } while (number <= 50);

    // Print the final sum
    std::cout << "Final Sum: " << sum << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}