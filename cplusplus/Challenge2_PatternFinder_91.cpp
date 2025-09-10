// Pattern Finder

#include <iostream>
// #include <cmath>
#include <string> // getline
// #include <iomanip>
// #include <clocale>
// #include <cstring> // 使用 strlen()
// using namespace std;

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    // system("chcp 65001 >> nul");

    // std::boolalpha 讓布林值以 "true" 或 "false" 的形式輸出，而不是 1 或 0
    std::cout << std::boolalpha;

    int n1;
    int n2;

    std::cin >> n1;
    std::cin >> n2;
    std::cin.ignore();
    int arr1[n1];
    int arr2[n2];

    for (int i = 0; i < n1; i++)
    {
        int val;
        std::cin >> val;
        arr1[i] = val;
    }

    for (int i = 0; i < n2; i++)
    {
        int val;
        std::cin >> val;
        arr2[i] = val;
    }

    // Write your code below using arr1, arr2, n1, n2
    bool found = false;
    if (n2 > n1)
    {
        std::cout << "false" << std::endl;
        return 0;
    }
    // for (int i = 0; i <= n1 - n2; i++)
    // {
    //     bool match = true;
    //     for (int j = 0; j < n2; j++)
    //     {
    //         if (arr1[i + j] != arr2[j])
    //         {
    //             match = false;
    //             break;
    //         }
    //     }
    //     if (match)
    //     {
    //         found = true;
    //         break;
    //     }
    // }
    // std::cout << found << std::endl;

    bool isConsecutive = false;
    for (int i = 0; i < n1; i++)
    {
        if (arr1[i] == arr2[0])
        {
            int ii = i + 1;
            for (int j = 1; j < n2; j++)
            {
                if (arr1[ii] != arr2[j])
                    break;
                if (j == n2 - 1)
                {
                    isConsecutive = true;
                }
                ii++;
            }
        }
        if (isConsecutive)
            break;
    }
    std::cout << isConsecutive << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}
