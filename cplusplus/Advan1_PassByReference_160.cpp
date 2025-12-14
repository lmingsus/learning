// Pass by Reference

/*
加上 & ，表示傳入參數的參考(reference)，
也就是說，傳入的參數會是原本變數的別名(alias)，
因此在函式內部修改參數的值，會直接影響到外部變數。
void doubleValue(int& number) {
    number = number * 2;  // 直接修改傳入的參數
}

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

void tripleValues(int &a, int &b, int &c)
{
    a = a * 3;
    b = b * 3;
    c = c * 3;
}

int main()
{
    // Read input values
    int value1, value2, value3;
    cin >> value1 >> value2 >> value3;

    // Print original values
    cout << "Original values: " << value1 << " " << value2 << " " << value3 << endl;

    // TODO: Call the tripleValues function here
    tripleValues(value1, value2, value3);

    // Print modified values
    cout << "Tripled values: " << value1 << " " << value2 << " " << value3 << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}