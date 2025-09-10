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

/*
「陣列退化 (Array Decay)」
在 C++ 中，當一個陣列（例如在 main 函式中宣告的 double arr[n]）
被用在大多數的表達式中時，它會自動「退化」或「轉換」成一個指向其第一個元素的指標。

這意味著在函式參數中，陣列實際上是作為指標來處理的，而不是作為完整的陣列。

void processArray(int arr[], int size);
void processArray(int* arr, int size); // 與上面那行完全相同


陣列退化會導致兩個關鍵的後果：

1. 無法獲取陣列大小：
在函式內部，無法使用 sizeof(arr) 來獲取陣列的大小，
因為 arr 現在是一個指標，而不是一個完整的陣列。
這就是為什麼我們需要額外傳遞一個 size 參數來告訴函式陣列的大小。

2. 直接操作原始資料：
因為函式接收到的是指向原始陣列記憶體位置的指標，
所以函式內部對 arr 的任何修改（例如 arr[0] = 99;）
都會直接改變 main 函式中原始陣列的內容。
這和傳遞一個普通變數（如 int 或 double）的行為完全不同，
傳遞一個普通變數是傳遞複本（pass-by-value）。
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

    int numbers[5] = {1, 2, 3, 4, 5};

    // 使用 std::size() 在陣列尚未退化前獲取其大小
    int array_size = std::size(numbers);

    // 將陣列和它的大小一起傳遞給函式
    processArray(numbers, array_size);

    int *newArr = processArray2(numbers);
    std::cout << "2. Array size in main: " << std::size(numbers) << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}
