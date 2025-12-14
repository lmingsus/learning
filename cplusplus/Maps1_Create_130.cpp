// Introducing std::map

/*
#include <map>

建立一個空的 map
std::map<std::string, int> score;

sscore["Alice"] = 95; // 新增一個鍵值對 ("Alice", 95)
score["Bob"] = 88;    // 新增一個鍵值對 ("Bob", 88)
scores["Carol"] = 92; // 新增一個鍵值對 ("Carol", 92)


score["Alice"] = 98; // 更新 "Alice" 的分數為 98
*/

#include <iostream>
// #include <cmath>
// #include <string> // getline
// #include <iomanip>
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

    // Read the number of students
    int n;
    cin >> n;

    // Create the map to store grades
    map<string, int> grades;

    // TODO: Write your code here
    // Read each student's name and score, then add to the map
    for (int i = 0; i < n; i++)
    {
        string student;
        int grade;
        cin >> student >> grade;
        grades[student] = grade; // Add or update the student's grade
    }

    // Print the results
    cout << "Student Grades:" << endl;
    // TODO: Use a range-based for loop to print each student's grade
    for (const auto &entry : grades)
    {
        cout << entry.first << ": " << entry.second << endl;
    }

    // Print total number of students
    cout << "Total students: " << grades.size() << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}