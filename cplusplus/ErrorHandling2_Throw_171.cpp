// The 'try' and 'catch' Blocks

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

void validateUser(const std::string &username, int age)
{
    // if (username.empty())
    // {
    //     throw "Username cannot be empty.";
    // }
    // if (age < 13)
    // {
    //     throw "Age must be at least 13";
    // }

    // 推薦的寫法：使用繼承自 std::exception 的物件
    if (username.empty())
        throw std::invalid_argument("Username cannot be empty.");
    if (age < 13)
        throw std::invalid_argument("Age must be at least 13");
}

int main()
{
    // Read input
    std::string username;
    int age;
    std::cin >> username;
    std::cin >> age;

    // TODO: Write your code here
    // Create the validateUser function and implement the validation logic
    // Use try-catch blocks to handle exceptions
    try
    {
        validateUser(username, age);
        std::cout << "User validation successful" << std::endl;
    }
    // catch (char const *e)
    // {
    //     std::cout << "Error: " << e << std::endl;
    // }
    // 使用推薦的寫法
    catch (const std::invalid_argument &e) // 捕捉為 const reference 是好習慣
    {
        std::cout << "Validation error: " << e.what() << std::endl;
    }
    catch (const std::exception &e) // 捕捉所有繼承自 std::exception 的異常
    {
        std::cout << "Error: " << e.what() << std::endl;
    }

    system("pause"); // 按任意鍵結束
    return 0;
}