/*
Prefix: increment/ decrement then return the new value
Postfix: return the current value then increment/ decrement


*/

#include <iostream>
#include <cmath>

int main()
{
    int x = 10;
    int y = 20;
    int z = 30;

    int a, b, c;

    // Type your code below
    a = x++;
    b = --y;
    c = z--;

    // Don't change the lines below
    std::cout << "a: " << a << std::endl;
    std::cout << "b: " << b << std::endl;
    std::cout << "c: " << c << std::endl;
    std::cout << "x: " << x << std::endl;
    std::cout << "y: " << y << std::endl;
    std::cout << "z: " << z << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}