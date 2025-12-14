// Introducing std::map

/*
#include <map>

建立一個空的 map
std::map<std::string, int> score;

sscore["Alice"] = 95; // 新增一個鍵值對 ("Alice", 95)
score["Bob"] = 88;    // 新增一個鍵值對 ("Bob", 88)
scores["Carol"] = 92; // 新增一個鍵值對 ("Carol", 92)

更新
score["Alice"] = 98; // 更新 "Alice" 的分數為 98

存取
int mayScore = scores["May"]; // 如果 "May" 不存在，會新增一個鍵值對 ("May", 0)，並回傳 0
自動建立非常方便，但如果只是想查詢而不想新增，這可能不是你想要的行為。
更安全的方式是使用 at() 方法：
int tomScore = scores.at("Tom"); // 如果 "Tom" 不存在，程式會拋出 std::out_of_range 異常而終止，更安全。

檢查
bool hasBob = scores.count("Bob"); // 如果 "Bob" 存在，回傳 1，否則回傳 0
bool hasBob = scores.find("Bob") != scores.end(); // 如果 "Bob" 存在，hasBob 為 true，否則為 false

刪除
scores.erase("Bob");  // 刪除鍵 "Bob" 及其對應的值
scores.erase("Mike"); // 如果鍵 "Mike" 不存在，erase 不會有任何作用或錯誤

迭代
for (const auto &entry : scores)
    cout << entry.first << ": " << entry.second << endl;
*/

#include <iostream>
// #include <cmath>
// #include <string> // getline
#include <iomanip> // For std::fixed and std::setprecision
// #include <clocale>
// #include <cstring> // 使用 strlen()
// #include <vector>
#include <map>
using namespace std;

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    // system("chcp 65001 >> nul");

    // std::boolalpha 讓布林值以 "true" 或 "false" 的形式輸出，而不是 1 或 0
    // std::cout << std::boolalpha;

    // Read the number of menu items
    int n;
    cin >> n;

    // Create the menu map
    map<string, double> menu;

    // Read menu items and prices
    for (int i = 0; i < n; i++)
    {
        string dish;
        double price;
        cin >> dish >> price;
        // TODO: Add the dish and price to the menu map
        menu[dish] = price;
    }

    // TODO: Print "Restaurant Menu:" header
    cout << "Restaurant Menu:" << endl;
    // TODO: Use range-based for loop to iterate through menu and print each item
    for (const auto &entry : menu)
        // Format: [dish]: $[price] with 2 decimal places
        cout << entry.first << ": $" << fixed << setprecision(2) << entry.second << endl;
    // TODO: Print total number of menu items
    cout << "Total menu items: " << menu.size() << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}