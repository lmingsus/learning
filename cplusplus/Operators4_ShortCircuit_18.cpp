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
    int a = 0;
    int b = 2;
    int c = 3;
    int d = 5;
    bool result0 = (a > 0 && b < 2) || (c < -5 && d < 10);
    cout << result0 << endl; // 0
    // 第 1 部分：計算 || 左側的表達式 (a > 0 && b < 2)
    // a > 0 為 false，短路發生！ 編譯器不會去計算 b < 2
    // 第 2 部分：計算整個 || 表達式，因為左側為 false，所以需要計算右側
    // 第 3 部分：計算 || 右側的表達式 (c < -5 && d < 10)
    //  c < -5，短路再次發生！ 編譯器不會去計算 d < 10。

    // Initialize variables
    bool isSunny = true;
    float windSpeed = 5.4f;
    float temperature = 23.f;
    float solarPanelOutput = 9.f;
    bool isCloudy = false;

    // The complete logical expression
    bool result = isSunny && windSpeed < 10 && solarPanelOutput < 15 && (temperature > 20 || !isCloudy);

    // Print results
    std::cout << "1. Is it sunny? " << std::boolalpha << isSunny << std::endl;
    std::cout << "2. Is wind speed safe? " << (windSpeed < 10) << std::endl;
    std::cout << "3. Do panels produce less? " << (solarPanelOutput < 15) << std::endl;
    std::cout << "4. Is temperature good OR no clouds? " << (temperature > 20 || !isCloudy) << std::endl;
    std::cout << "5. Final result: " << result << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}