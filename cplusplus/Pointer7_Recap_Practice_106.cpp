// Recap - Pointer Practice

/*
int* ptr = new int;  // 配置一個整數的動態記憶體，回傳該記憶體位置的指標並存入 ptr
*ptr = 42;           // 將值 42 存入該記憶體位置

使用 new int 意味著您的程式會不斷地消耗電腦的 RAM。
如果洩漏嚴重，最終會耗盡所有可用記憶體，導致程式執行速度變慢，甚至整個系統崩潰。

delete ptr;          // 釋放該記憶體，否則會發生記憶體外洩 (Memory Leak)

在 delete ptr; 執行後的瞬間，記憶體中代表 42 的那些位元 (bits) 可能還在那裡，還沒有被覆寫。
但是，這些位元已經不再屬於您的程式，因為您已經釋放了那塊記憶體。

在 delete ptr; 之後，指標 ptr 變成了一個懸掛指標 (Dangling Pointer)。
它仍然儲存著那個記憶體的位址，但那個位址對您來說已經是無效的、非法的。
如果您嘗試透過這個懸掛指標來存取或修改那塊記憶體，會導致未定義行為 (Undefined Behavior)。
未定義行為的結果可能是程式崩潰、資料損壞，甚至看似正常運作但實際上已經產生錯誤。
為了避免懸掛指標的問題，通常在 delete 之後，會將指標設為 nullptr。

ptr = nullptr; // 現在 ptr 不再指向任何有效的記憶體位置
*/

/*
每個 new 都應該有一個對應的 delete。
否則會發生記憶體外洩 (Memory Leak)。
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
