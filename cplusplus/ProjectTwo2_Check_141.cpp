// Recap - Word Frequency

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
// #include <iomanip> // For std::fixed and std::setprecision
// #include <clocale>
// #include <cstring> // 使用 strlen()
// #include <vector>
#include <map>
using namespace std;

int main()
{
    // TODO: Write your code below
    std::map<std::string, int> inventory;
    // inventory["Laptops"] = 15;
    // inventory["Mice"] = 42;
    // inventory["Keyboards"] = 28;
    // inventory["Monitors"] = 12;
    inventory["apples"] = 50;
    inventory["bananas"] = 30;
    inventory["oranges"] = 25;
    inventory["grapes"] = 40; // new
    // cout << "Initial Inventory Setup:" << endl;
    // for (const auto &entry : inventory)
    //     cout << entry.first << ": " << entry.second << endl;
    // cout << "Inventory system is ready!" << endl;

    // int numOper;
    // cin >> numOper;
    // for (int i = 0; i < numOper; i++)
    // {
    //     int quantity;
    //     string item;
    //     cin >> item>> quantity;
    //     cout << "Added " << quantity << " " << item;
    //     inventory[item] += quantity;
    //     cout << ". New total: "  << inventory[item] << endl;
    // }
    // cout << "Final Inventory:" << endl;
    // for (const auto &entry : inventory)
    //     cout << entry.first << ": " << entry.second << endl;

    int numCheck;
    cin >> numCheck;
    for (int i = 0; i < numCheck; i++)
    {
        string itemCheck;
        cin >> itemCheck;
        if (inventory.count(itemCheck))
            cout << itemCheck << ": " << inventory[itemCheck] << " in stock" << endl;
        else
            cout << itemCheck << ": Item not found" << endl;
    }
    cout << "Total items in inventory: " << inventory.size() << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}