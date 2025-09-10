/*
result = 10 % 3; // 1

#include <cmath>
double result = fmod(5.2, 2.0);  // result is 1.2
*/

#include <iostream>
#include <cmath>

int main()
{
    // Type your code below
    int a = 9;
    double b = 2.6;
    int c = 11;
    int d = a % 2;
    int e = a % 3;
    double f = fmod(b, 1.5);
    double g = fmod(b, 3.9);
    int h = c % 10;

    // Don't change the line below
    std::cout << "a = " << a << std::endl;
    std::cout << "b = " << b << std::endl;
    std::cout << "c = " << c << std::endl;
    std::cout << "d = " << d << std::endl;
    std::cout << "e = " << e << std::endl;
    std::cout << "f = " << f << std::endl;
    std::cout << "g = " << g << std::endl;
    std::cout << "h = " << h << std::endl;
    system("pause"); // 按任意鍵結束
    return 0;
}