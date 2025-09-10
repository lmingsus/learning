// Dereference Operator

/*
int number = 42;
int* ptr = &number;  // ptr now stores the address of number
int value = *ptr;    // value now contains 42


*ptr = 100;  // Changes number to 100
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

    int score = 85;
    int *scorePtr = &score;
    cout << "scorePtr: " << scorePtr << endl;
    cout << "&score: " << &score << endl;
    cout << "*&score: " << *&score << endl;

    cout << "*scorePtr: " << *scorePtr << endl;
    cout << "*&*scorePtr: " << *&*scorePtr << endl;

    *scorePtr = 100; // Changes score to 100
    cout << "New Value: " << *scorePtr << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}
