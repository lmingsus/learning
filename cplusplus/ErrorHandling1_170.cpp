// The 'throw' Keyword

/*
try {
    Code that might throw an exception
} catch (exception_type e) {
    Code to handle the exception
}
*/

/*
當我們使用 std::stoi 來將字串轉換為整數時，
如果字串中包含非數字字元，會拋出一個 std::invalid_argument 異常。

try {
    std::string input = "abc";
    int number = std::stoi(input);  // This will throw an exception
    std::cout << "Number: " << number << std::endl;
} catch (std::invalid_argument& e) {
    std::cout << "Invalid input! Please enter a valid number." << std::endl;
}
*/

#include <iostream>
// #include <cmath>
#include <string> // std::string, std::stoi, std::getline
// #include <iomanip> // For std::fixed and std::setprecision
// #include <clocale>
// #include <cstring> // 使用 strlen()
// #include <vector>
// #include <map>
// #include <set>
// #include <vector>
// #include <algorithm> // std::sort
#include <stdexcept> // std::invalid_argument
// using namespace std;

int main()
{
    // Read input
    std::string userInput;
    std::cin >> userInput;

    // TODO: Write your code below
    // Use try-catch blocks with std::stoi to convert the string
    try
    {
        int number = std::stoi(userInput);
        std::cout << "Valid number: " << number << std::endl;
    }
    // catch (std::invalid_argument &e)
    catch (const std::invalid_argument &e) // 捕捉為 const reference 是好習慣
    {
        std::cout << "Error: Invalid input" << std::endl;
        // 使用 e.what() 來印出由函式庫提供的詳細錯誤訊息
        std::cout << "Error details: " << e.what() << std::endl;
    }

    system("pause"); // 按任意鍵結束
    return 0;
}