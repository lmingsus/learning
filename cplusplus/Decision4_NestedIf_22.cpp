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
    int age, height;
    bool hasAdult;
    std::cin >> age >> height >> hasAdult; // Don't change this line
    std::string result = "";

    // Write your code below
    if (age < 12)
    {
        result = "Sorry, you are too young";
    }
    else if (height <= 150)
    {
        result = "Sorry, you are not tall enough";
    }
    // else if (age < 15 && !hasAdult)
    // {
    //     result = "Sorry, you need an adult with you";
    // }
    // else if (age < 15)
    // {
    //     result = "You can ride with adult supervision!";
    // }
    // else
    // {
    //     result = "You can ride by yourself!";
    // }
    else
    {
        if (age < 15)
        {
            // 將與 hasAdult 相關的邏輯組織在一起。
            result = hasAdult ? "You can ride with adult supervision!" : "Sorry, you need an adult with you";
        }
        else // age >= 15
        {
            result = "You can ride by yourself!";
        }
    }
    std::cout << result << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}