// Challenge

/*
Create a function named calculate that takes two integers and a character as arguments (parameters). The character represents an arithmetic operation: +, -, *, or /. Perform the corresponding operation on the two integers and print the result in the format: [num1] [operation] [num2] = [result]. For division (/), perform integer division (ignore remainders).
*/

#include <iostream>
// #include <cmath>
#include <string> // getline
// #include <iomanip>
// using namespace std;
// #include <io.h>    // 為了使用 _setmode
// #include <fcntl.h> // 為了使用 _O_U16TEXT
// #include <clocale>

void calculate(int a, int b, char op)
{
    int result;
    switch (op)
    {
    case '+':
        result = a + b;
        break;
    case '-':
        result = a - b;
        break;
    case '*':
        result = a * b;
        break;
    case '/':
        result = a / b;
        break;
    default:
        break;
    }
    std::cout << a << " " << op << " " << b << " = " << result << std::endl;
    // if (op == '+')
    // {
    //     std::cout << a << " + " << b << " = " << (a + b) << std::endl;
    // }
    // else if (op == '-')
    // {
    //     std::cout << a << " - " << b << " = " << (a - b) << std::endl;
    // }
    // else if (op == '*')
    // {
    //     std::cout << a << " * " << b << " = " << (a * b) << std::endl;
    // }
    // else if (op == '/')
    // {
    //     std::cout << a << " / " << b << " = " << (a / b) << std::endl;
    // }
    // else
    // {
    //     std::cout << "Invalid operation" << std::endl;
    // }
    return;
}

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    system("chcp 65001");

    // Write code here
    int num1, num2;
    char operation;
    std::cin >> num1 >> operation >> num2;
    calculate(num1, num2, operation);

    system("pause"); // 按任意鍵結束
    return 0;
}
