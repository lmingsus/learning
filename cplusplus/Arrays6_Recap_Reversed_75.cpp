// Declaring Arrays

/*
讓編譯器自動推斷大小：
int numbers[] = {1, 2, 3, 4, 5};

宣告一個未初始化的陣，陣列內容是未定義的垃圾值
int numbers[5];

宣告並使用初始化列表，未提供值的元素會被自動初始化為 0
int numbers[5] = {10, 20};

C++11 的列表初始化語法，將所有元素初始化為 0
int numbers[5] {0};

int length = std::size(numbers);
*/

#include <iostream>
// #include <cmath>
#include <string> // getline
// #include <iomanip>
// using namespace std;
// #include <clocale>

// 增加一個 'size' 參數來接收陣列大小
// 當您將一個 C-style 陣列（如 numbers）作為參數傳遞給函式時，它會發生「陣列退化 (array decay)」。
// 這意味著函式接收到的不再是一個完整的陣列，而只是一個指向陣列第一個元素的指標。
void processArray(int arr[], int size)
{
    // 現在我們使用傳入的 size，而不是試圖用 std::size() 推斷
    std::cout << "1. Array size inside function: " << size << std::endl;
}

// 返回陣列的指標
int *processArray2(int arr[])
{
    return arr;
}

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    // system("chcp 65001");
    int n;

    std::cin >> n;
    std::cin.ignore();
    double arr[n];

    for (int i = 0; i < n; i++)
    {
        double val;
        std::cin >> val;
        arr[i] = val;
    }

    double reverseArr[n];
    // Write your code below
    for (int i = 0; i < n; ++i)
    {
        reverseArr[n - 1 - i] = arr[i];
    }

    for (int i = 0; i < n; i++)
    {
        std::cout << reverseArr[i] << std::endl;
    }

    system("pause"); // 按任意鍵結束
    return 0;
}
