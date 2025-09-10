/*

*/

/*


*/

#include <iostream>
// #include <cmath>
// #include <string>
using namespace std;

int main()
{
    int month;
    // std::cin >> month;
    std::string season = "";

    month = 1;
    // Write your code below
    switch (month)
    {
    case 12:
    case 1:
    case 2:
        season = "Winter";
        // break;  // The next case will be executed regardless of its value
    case 3:
    case 4:
    case 5:
        season = "Spring"; // 會顯示 Spring
        break;
    case 6:
    case 7:
    case 8:
        season = "Summer";
        break;
    case 9:
    case 10:
    case 11:
        season = "Autumn";
        break;
    default:
        season = "Invalid month";
    }

    std::cout << season << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}