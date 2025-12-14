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

/*
各種異常類型的捕捉
try {
    ......
} catch (std::invalid_argument& e) {
    std::cout << "Invalid input format!" << std::endl;
} catch (std::out_of_range& e) {
    std::cout << "Number is too large!" << std::endl;
} catch (const char* msg) {
    std::cout << "Custom error: " << msg << std::endl;
}
使用推薦的寫法
catch (const std::invalid_argument &e)           // 捕捉為 const reference 是好習慣
{
    std::cout << "Validation error: " << e.what() << std::endl;
}
catch (const std::exception &e)                  // 捕捉所有繼承自 std::exception 的異常
{
    std::cout << "Error: " << e.what() << std::endl;
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

void processData(const std::string &operation, const std::string &data)
{
    if (operation == "convert")
    {
        int result = std::stoi(data);
        std::cout << "Result: " << result << std::endl;
    }
    else if (operation == "divide")
    {
        int result = 100 / std::stoi(data);
        std::cout << "Result: " << result << std::endl;
    }
    else if (operation == "access")
    {
        int index = std::stoi(data);
        std::string hello = "Hello";
        char result = hello.at(index);
        std::cout << "Result: " << result << std::endl;
    }
}

int main()
{
    // Read input
    std::string operation;
    std::string data;
    std::cin >> operation;
    std::cin >> data;
    try
    {
        processData(operation, data);
    }
    catch (const std::invalid_argument &e)
    {
        std::cout << "Invalid argument error" << std::endl;
    }
    catch (const std::out_of_range &e)
    {
        std::cout << "Out of range error" << std::endl;
    }
    catch (const std::exception &e)
    {
        std::cout << "Custom error: " << e.what() << std::endl;
    }

    system("pause"); // 按任意鍵結束
    return 0;
}