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
    int number;
    // std::cin >> number;
    number = -5;
    std::string result = "";

    // Write your code below
    result = (number > 0) ? "positive" : (number < 0) ? "negative"
                                                      : "zero";

    std::cout << "The number is " << result << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}