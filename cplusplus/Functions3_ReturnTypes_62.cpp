// Nested Loops

/*
access_modifier return_type method_name(parameters) {
    code
}
*/

/*
Each test case has three inputs.

The first input indicates how many times to do iterations, and the last two inputs are numbers that we will do operations on.

Create a function that receives two arguments and returns the bigger number of the two. if both are equal then return one of them.

Iterate iterations times and for each iteration do:

Call the function with num1, num2, and save the result in a variable.
Divide the bigger number of the two by 2, and then replace the original larger variable with the new result value.
print the new value.
Continue doing it until the program iterated iterations times or one of the numbers is smaller than 2.
*/

#include <iostream>
// #include <cmath>
// #include <string>
// #include <iomanip>
// using namespace std;

// Function declaration
double getBigger(double a, double b)
{
    // return (a > b) ? a : b;
    // 使用 std::max 是更慣用且可讀性更高的 C++ 寫法。
    return std::max(a, b);
}

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    system("chcp 65001");

    int iterations;
    double num1, num2;
    std::cin >> iterations >> num1 >> num2;

    for (int i = 0; i < iterations; i++)
    {
        double bigger = getBigger(num1, num2);
        // if (bigger == num1)
        // {
        //     num1 = bigger / 2;
        //     std::cout << num1 << std::endl;
        // }
        // else
        // {
        //     num2 = bigger / 2;
        //     std::cout << num2 << std::endl;
        // }
        double &bigger_ref = (num1 > num2) ? num1 : num2;
        bigger_ref /= 2;
        std::cout << bigger_ref << std::endl;

        if (bigger < 4)
            break;
    }

    system("pause"); // 按任意鍵結束
    return 0;
}
