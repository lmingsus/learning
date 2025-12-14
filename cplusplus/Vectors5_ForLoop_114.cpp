// Adding Elements

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


使用參考 reference，直接指向 cities 向量中對應的原始元素。
for (const string& city : cities) {
    cout << city << endl;
}
第一次迴圈，city 就是 cities[0] 的別名
第二次迴圈，city 就是 cities[1] 的別名，以此類推。
優點：完全沒有複製操作發生。您是直接透過別名 city 來存取原始資料，這非常高效。

如果沒有 & 的情況，
在迴圈的每一次迭代中，程式都會從 cities 向量中取出一個字串元素，
然後完整地複製一份，並將這個複本命名為 city。
對於像 std::string 這樣可能很長的物件，這會造成不必要的記憶體和 CPU 時間浪費，降低程式效能。
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

    // Read the number of cities
    int n;
    cin >> n;

    // Create a vector to store city names
    vector<string> cities;

    // Read city names and add them to the vector
    for (int i = 0; i < n; i++)
    {
        string city;
        cin >> city;
        cities.push_back(city);
    }

    // TODO: Write your code below
    // Use a range-based for loop to iterate through the cities vector
    // Print each city with its length using the specified format
    // After the loop, print the total number of cities processed
    for (const std::string &city : cities)
    {
        cout << "City: " << city;
        cout << " (Length: " << city.length() << ")" << endl;
    }
    cout << "Total cities processed: " << cities.size() << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}
