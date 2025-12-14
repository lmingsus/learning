// Create Set & Add Elements

/*
std::set<int> numbers;
唯一性 (Uniqueness)：集合中的元素不會重複。
自動排序 (Automatic Sorting)：預設是從小到大（升序）排列。
高效查找 (Efficient Lookups)：由於內部是經過排序的（通常使用紅黑樹這種資料結構實現），std::set 可以非常快速地（以對數時間複雜度 O(log n)）進行查找、插入和刪除操作。

numbers.insert(5);
numbers.insert(2);
numbers.insert(8);

numbers.erase(2); // 如果元素 2 不存在，erase 不會有任何作用或錯誤

numbers.size() // 回傳集合中元素的數量

for (const int& elem : numbers) {
    cout << " " << elem;
}


if (numbers.count(2)) // 只會回傳 1（存在）或 0（不存在）
    cout << "2 is in the set" << endl;

if (numbers.find(3) != numbers.end())
    cout << "3 is in the set" << endl;


auto it = numbers.find(3);  // 在集合中尋找指定的元素，回傳值是一個「迭代器 (iterator)」
如果找到了 3：find(3) 會回傳一個指向 3 這個元素的迭代器。
如果沒找到 3：find(3) 會回傳一個特殊的迭代器，這個迭代器和 numbers.end() 回傳的迭代器是相同的。

numbers.end()  // 回傳一個指向「集合結尾之後」位置的特殊迭代器。
這個「結尾之後」的迭代器本身不代表任何有效的元素，它只是一個標記，用來表示「我們已經遍歷完所有元素了」或「搜尋失敗了」。

*/

#include <iostream>
// #include <cmath>
// #include <string> // getline
// #include <iomanip> // For std::fixed and std::setprecision
// #include <clocale>
// #include <cstring> // 使用 strlen()
// #include <vector>
// #include <map>
#include <set>
using namespace std;

int main()
{
    // Read the number of words
    int n;
    cin >> n;

    // Create an empty set to store words
    set<string> wordSet;

    // TODO: Write your code here
    // Read n words and insert them into the set
    for (int i = 0; i < n; i++)
    {
        string input;
        cin >> input;
        wordSet.insert(input);
    }
    // Use a range-based for loop to iterate through the set and print each word
    for (const string &elem : wordSet)
    {
        cout << elem << endl;
    }
    // Print the total count of unique words
    cout << "Total unique words: " << wordSet.size() << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}