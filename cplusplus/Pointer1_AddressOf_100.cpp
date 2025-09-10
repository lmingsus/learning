// Address-Of Operator

/*
int number = 42;
int* ptr = &number;  // ptr now stores the address of number

&number gets the memory address of the variable number
*/

#include <iostream>
// #include <cmath>
// #include <string> // getline
// #include <iomanip>
// #include <clocale>
// #include <cstring> // 使用 strlen()
using namespace std;

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    // system("chcp 65001 >> nul");

    // std::boolalpha 讓布林值以 "true" 或 "false" 的形式輸出，而不是 1 或 0
    // std::cout << std::boolalpha;

    // Read input values
    int initialValue, newValue;
    cin >> initialValue;
    cin >> newValue;

    // TODO: Write your code below
    // 1. Declare an integer variable named 'score' and initialize it with initialValue
    int score = initialValue;
    // 2. Create a pointer named 'scorePtr' that points to the score variable
    int *scorePtr = &score;
    // 3. Print the original value, modify through pointer, and print results
    cout << "Original score: " << *scorePtr << endl;
    *scorePtr = newValue;
    cout << "Modified score: " << *scorePtr << endl;
    cout << "Pointer address: " << scorePtr << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}
