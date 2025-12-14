// Creating a Vector

/*
C-style arrays 是固定長度，手動管理記憶體，不儲存長度資訊，傳遞時會退化為指標。
std::vector 是動態長度，自動管理記憶體，內部儲存長度資訊，傳遞時保持為物件。
*/

/*
#include <vector>
std::vector<資料型別> 變數名稱;

std::vector<int> scores;          // 一個存放整數的 vector
std::vector<double> prices;       // 一個存放浮點數的 vector
std::vector<std::string> names;   // 一個存放字串的 vector

std::vector<int> scores = {85, 92, 78, 96, 88}; // 使用初始化列表來初始化 vector


push_back(value)：在 vector 的尾端加入一個新元素。
scores.push_back(95); // scores 現在是 {95}
scores.push_back(88); // scores 現在是 {95, 88}

int firstScore = scores[0]; // 取得第一個元素 (95)

int secondScore = scores.at(1); // 取得第二個元素 (88)
同樣用索引存取，但會進行邊界檢查。
如果索引越界，程式會拋出 std::out_of_range 異常而終止，更安全。

int firstScore = scores.front();  // 取得第一個元素 (95)
int lastScore = scores.back();    // 取得最後一個元素 (88)

int sizeScore = scores.size();    // 回傳 vector 中元素的數量。
bool isEmpty = scores.empty();    // 如果 vector 為空，回傳 true，否則回傳 false。
scores.clear();                   // 清空 vector 中的所有元素，變成空的 vector。
scores.pop_back();                // 移除 vector 中的最後一個元素。
scores.resize(10);                // 將 vector 的大小調整為 10。如果新的大小大於目前大小，新增的元素會被預設初始化。
scores.resize(3);                 // 將 vector 的大小調整為 3，超過的元素會被移除。


for (int val : scores) {
    std::cout << val << std::endl;
}
*/

#include <iostream>
// #include <cmath>
// #include <string> // getline
// #include <iomanip>
// #include <clocale>
// #include <cstring> // 使用 strlen()
#include <vector>
using namespace std;

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    // system("chcp 65001 >> nul");

    // std::boolalpha 讓布林值以 "true" 或 "false" 的形式輸出，而不是 1 或 0
    // std::cout << std::boolalpha;

    // Read input values
    int val1, val2, val3, val4, val5;
    cin >> val1 >> val2 >> val3 >> val4 >> val5;

    // TODO: Write your code below
    // Create a vector named 'numbers' and initialize it with the input values
    // Print each element using the required format
    // Print the vector size
    vector<int> numbers = {val1, val2, val3, val4, val5};
    for (int i = 0; i < numbers.size(); i++)
    {
        cout << "Element " << i << ": " << numbers[i] << endl;
    }
    cout << "Vector size: " << numbers.size() << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}
