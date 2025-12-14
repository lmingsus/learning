//

/*
C-style arrays 是固定長度，手動管理記憶體，不儲存長度資訊，傳遞時會退化為指標。
std::vector 是動態長度，自動管理記憶體，內部儲存長度資訊，傳遞時保持為物件。
std::set 是一種標準模板庫，提供了一種儲存唯一元素的容器，並自動排序。
*/

/*
std::set<int> numbers = {10, 20, 30, 40};
numbers.erase(20);  // Removes the element 20
numbers.erase(50);  // 將會什麼事都不做，因為 50 不在集合中
*/

#include <iostream>
// #include <cmath>
// #include <string> // getline
// #include <iomanip>
// #include <clocale>
// #include <cstring> // 使用 strlen()
// #include <vector>
#include <set>
using namespace std;

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    // system("chcp 65001 >> nul");

    // std::boolalpha 讓布林值以 "true" 或 "false" 的形式輸出，而不是 1 或 0
    // std::cout << std::boolalpha;

    // Read number of elements to add
    int n;
    cin >> n;

    // Create an empty set
    set<int> mySet;

    // Read and insert n elements
    for (int i = 0; i < n; i++)
    {
        int element;
        cin >> element;
        // Insert element into set
        mySet.insert(element);
    }

    // Read number of elements to remove
    int m;
    cin >> m;

    // TODO: Write your code below
    // 1. Print initial set size
    cout << "Initial size: " << mySet.size() << endl;
    // 2. For each element to remove, use .erase() and print size after each removal
    for (int i = 0; i < m; i++)
    {
        int toRemove;
        cin >> toRemove;
        mySet.erase(toRemove);
        cout << "After removing " << toRemove << ": size = " << mySet.size() << endl;
    }
    // 3. Print remaining elements in the set
    cout << "Remaining elements:";
    for (const int &elem : mySet)
    {
        cout << " " << elem;
    }
    cout << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}
