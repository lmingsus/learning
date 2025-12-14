// Intro Lambda Expressions

/*
Lambda 運算式 (Lambda Expressions) 是 C++11 引入的一個強大特性

[capture_clause](parameters) -> return_type {
    function body
};

[] - 捕獲子句 (Capture Clause)
指定 Lambda 函式可以「捕獲」或存取其所在範圍 (surrounding scope) 中的哪些變數
    []：不捕獲任何外部變數。
    [=]：以傳值 (by value) 方式捕獲所有外部變數（建立副本）。
    [&]：以傳參考 (by reference) 方式捕獲所有外部變數（使用別名）。
    [var]：只以傳值方式捕獲變數 var。
    [&var]：只以傳參考方式捕獲變數 var。
    [this]：捕獲目前物件的 this 指標。

() - 參數列表 (Parameter List)
和一般函式的參數列表完全一樣。您可以定義 Lambda 函式需要接收的參數。
如果不需要參數，可以省略 ()。

-> return_type - 回傳類型 (Return Type)
是可選的。
如果 Lambda 的函式主體只有一個 return 陳述式，或者沒有回傳值，編譯器可以自動推導回傳型別。

{ } - 函式主體 (Function Body)
在這裡您可以撰寫 Lambda 函式的實際程式碼邏輯。
*/

/*
傳統的具名函式
void tripleValues(int &a, int &b, int &c)
{
    a = a * 3;
    b = b * 3;
    c = c * 3;
}
在 main 中呼叫
tripleValues(value1, value2, value3);


使用 Lambda
auto triple = [](int &val) {
    val *= 3;
};
triple(value1);

立即執行的 Lambda
[]() {
    std::cout << "Immediate execution!" << std::endl;
}();
*/

/*
auto addNumbers = [](int a, int b) {
    std::cout << "Sum: " << (a + b) << std::endl;
};

addNumbers(5, 3);  // Prints: Sum: 8

立即執行的 Lambda
[](int x, int y) {
    std::cout << "Product: " << (x * y) << std::endl;
}(4, 7);  // Prints: Product: 28
*/

/*
使用 -> return_type 指定回傳類型
auto multiply = [](int a, int b) -> int {
    return a * b;
};
int result = multiply(4, 5); // result 會是 20
*/

#include <iostream>
// #include <cmath>
// #include <string> // getline
// #include <iomanip> // For std::fixed and std::setprecision
// #include <clocale>
// #include <cstring> // 使用 strlen()
// #include <vector>
// #include <map>
// #include <set>
using namespace std;

int main()
{
    // Read input
    double num1, num2;
    char operation;
    cin >> num1 >> num2 >> operation;

    // TODO: Write your code here
    // Create a lambda expression named 'calculate' that takes two double parameters and a char parameter
    // Use the arrow syntax -> double to specify return type
    // Use conditional logic inside the lambda to perform the operation and return the result
    auto calculate = [](double a, double b, char op) -> double
    {
        switch (op)
        {
        case '+':
            return a + b;
        case '-':
            return a - b;
        case '*':
            return a * b;
        case '/':
            if (b != 0)
                return a / b;
        default:
            return 0;
        }
    };
    // TODO: Call the lambda with input values and store the result
    double result = calculate(num1, num2, operation);
    // Output the result
    cout << "Result: " << result << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}