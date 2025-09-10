// Null Pointers

/*
int number = 42;
int* ptr = &number;  // ptr now stores the address of number
int value = *ptr;    // value now contains 42

*ptr = 100;  // Changes number to 100
*/

/*
星號 (*) 的雙重意義

1. 在宣告中：表示「...的指標」 (Pointer to...)
「*」出現在變數宣告的型別旁邊時，它用來宣告一個指標變數
告訴編譯器：「這個變數儲存的不是一個值，而是一個記憶體位址。」

2. 在使用中：表示「解參考」 (Dereference)
當 * 出現在一個已經宣告過的指標變數前面時，它的意義變為一個運算子，稱為「解參考運算子」。
作用是「取得指標所指向位址上的值」。
*/

/*
int* ptr;  // 沒有初始化的指標，值是隨機的，可能指向任何地方
這個位址被稱為「野指標 (Wild Pointer)」。

一個 null pointer 是一個不指向任何有效記憶體位置的指標。它通常用來表示「沒有值」或「不指向任何東西」。
int* ptr = nullptr;  // ptr is now a null pointer
`nullptr` 是 C++11 引入的關鍵字，用來表示空指標。它比傳統的 `NULL` 更安全，因為 `NULL` 通常被定義為 0，可能會引起混淆。

永遠不要使用未初始化的指標。
如果您還不知道要指向哪裡，就將它初始化為空指標 nullptr。

在賦予它一個有效位址之前，不要使用它，
1. 讓 ptr 指向一個已存在的變數：int* ptr = &myValue;
2. 或是動態配置一塊記憶體空間：int* ptr = new int;
if (ptr != nullptr) {
    *ptr = 100; // 只有在 ptr 指向某處時才安全
}
*/

/*
string* ptr = nullptr;  // 宣告了一個指向 std::string 的指標 ptr，並將它初始化為 nullptr
cout << "ptr: " << ptr << endl; // 印出指標 ptr 本身儲存的值。
對於一個空指標，通常會印出 0 或 0x0，表示它不指向任何記憶體位址。

*ptr = "100"; // 試圖將字串 "100" 寫入這個禁止存取的位置
因為 ptr 是 nullptr，所以它指向的是一個無效的、受作業系統保護的記憶體區域（通常是位址 0）。
正確的做法：在使用指標寫入資料之前，必須確保它指向一個有效的、已經存在的物件。
std::string myText;          // 先建立一個實際的 string 物件
std::string* ptr = &myText;  // 然後讓指標指向這個物件
*ptr = "100";                // 現在這是安全的，因為 ptr 指向一個有效的 string 物件
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

    // Read input
    string input;
    cin >> input;

    // Declare the data variable
    int data = 42;

    // TODO: Write your code here
    // - Declare a pointer named ptr
    // - Check the input and assign appropriate value to ptr
    // - Use if-statement to safely check and use the pointer
    int *ptr = nullptr;
    if (input == "valid")
        ptr = &data;

    if (ptr != nullptr)
        cout << "Value: " << *ptr << endl;
    else
        cout << "Pointer is null - cannot dereference" << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}
