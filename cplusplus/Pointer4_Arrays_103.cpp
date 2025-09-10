// Pointers and Arrays

/*
int numbers[5] = {10, 20, 30, 40, 50};
numbers 是這個陣列的名稱。它代表了一整塊連續的記憶體空間，這塊空間的大小足以存放 5 個整數。
陣列的名稱在大多數情況下，會自動「退化 (decay)」成一個指向其第一個元素的指標。
int* ptr = numbers;  // ptr 現在指向陣列的第一個元素 numbers[0]
在編譯器眼中，其實就等同於：int *ptr = &numbers[0];

&numbers[0] 這個位址的型別是 int* (指向整數的指標），
指標變數 ptr 的型別也是 int* ，
因為兩邊的型別完全匹配，所以這個賦值是完全合法的。

ptr++;                  // ptr 現在指向 numbers[1]，
因為位址向前移動 sizeof(int) 個位元組，剛好到達下一個整數的位置。

int value = *(ptr + 2); // value 現在是 40，因為 ptr + 2 指向 numbers[3]
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

    // Given array
    int values[6] = {15, 23, 8, 42, 17, 31};

    // TODO: Create a pointer named 'ptr' that points to the first element of the array
    int *ptr = values;
    // TODO: Use a loop to iterate through all 6 elements using pointer arithmetic
    // TODO: Print each element by dereferencing the pointer
    // TODO: Move the pointer to the next element using pointer arithmetic
    for (int i = 0; i < 6; i++)
        cout << "Element: " << *(ptr + i) << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}
