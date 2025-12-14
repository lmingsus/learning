// Recap - Vector Operations

#include <iostream>
// #include <cmath>
#include <string> // getline
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

    vector<string> tasks;
    cout << "Welcome to Task List Tool!" << endl;
    cout << "\nMenu Options:\n1. Add Task\n2. View Tasks\n3. Remove Task\n4. Quit" << endl;
    cout << "\nTask list system initialized and ready!" << endl;

    while (true)
    {
        cout << "Choose an option: ";
        int taskNum;
        cin >> taskNum;
        cin.ignore();

        if (taskNum == 4)
        {
            cout << "Thank you for using Task List Tool!" << endl;
            break;
        }
        else if (taskNum == 1)
        {
            string task;
            getline(cin, task);
            tasks.push_back(task);
            cout << "Task \"" << task << "\" added successfully!" << endl;
            cout << "Total tasks: " << tasks.size() << endl;
        }
        else if (taskNum == 2)
        {
            if (tasks.empty())
                cout << "No tasks available." << endl;
            else
            {
                cout << "Your Tasks:" << endl;
                for (int i = 0; i < tasks.size(); i++)
                {
                    cout << i + 1 << ". " << tasks.at(i) << endl;
                }
                cout << "Total tasks: " << tasks.size() << endl;
            }
        }
        else if (taskNum == 3)
        {
            int removeIndex;
            cin >> removeIndex;
            if (removeIndex < 1 || removeIndex > tasks.size())
            {
                cout << "Error: Invalid task number. Please enter a number between 1 and " << tasks.size() << "." << endl;
            }
            else
            {
                string removeTask = tasks.at(removeIndex - 1);
                tasks.erase(tasks.begin() + removeIndex - 1);
                cout << "Task \"" << removeTask << "\" removed successfully!" << endl;
                if (tasks.empty())
                    cout << "No tasks remaining." << endl;
                else
                {
                    cout << "Remaining Tasks:" << endl;
                    for (int i = 0; i < tasks.size(); i++)
                    {
                        cout << i + 1 << ". " << tasks.at(i) << endl;
                    }
                }
                cout << "Total tasks: " << tasks.size() << endl;
            }
        }
        else
            cout << "Invalid choice. Please try again." << endl;
    }

    system("pause"); // 按任意鍵結束
    return 0;
}
