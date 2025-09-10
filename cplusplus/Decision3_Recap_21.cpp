/*
variable = (condition) ? value_if_true : value_if_false;
*/

/*
int age = 20;
std::string message = (age >= 18) ? "Adult" : "Minor";

std::string unit = (isCelsius) ? "Celsius" : "Fahrenheit";
*/

#include <iostream>
// #include <cmath>
// #include <string>
using namespace std;

int main()
{
    double n1, n2;
    char op;
    std::cin >> n1 >> n2 >> op;

    // Write your code below
    double result = 0;
    // if (op == '+')
    // {
    //     result = n1 + n2;
    // }
    // else if (op == '-')
    // {
    //     result = n1 - n2;
    // }
    // else if (op == '/')
    // {
    //     result = n1 / n2;
    // }
    // else if (op == '*')
    // {
    //     result = n1 * n2;
    // }

    // 使用 switch 陳述式更適合這種單一變數對多個值的判斷，
    // 程式碼結構更清晰，且容易擴充。
    switch (op)
    {
    case '+':
        result = n1 + n2;
        break;
    case '-':
        result = n1 - n2;
        break;
    case '*':
        result = n1 * n2;
        break;
    case '/':
        // 增加對除以零的檢查，讓程式更穩健。
        if (n2 != 0)
        {
            result = n1 / n2;
        }
        else
        {
            std::cerr << "Error: Division by zero is not allowed." << std::endl;
        }
        break;
    default:
        // 處理所有未預期的運算子，增加程式的穩健性。
        std::cerr << "Error: Invalid operator '" << op << "'." << std::endl;
        break;
    }

    std::cout << result << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}