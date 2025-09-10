// Recap - Validation Function

#include <iostream>
// #include <cmath>
#include <string> // getline
// #include <iomanip>
// using namespace std;
#include <io.h>    // 為了使用 _setmode
#include <fcntl.h> // 為了使用 _O_U16TEXT
#include <clocale>

void printNTimes(const std::wstring &message, int n)
{
    // const 關鍵字則確保函式內部不會意外修改到原始的 msg 字串，增加了程式的安全性。
    // & 表示以「參考 (reference)」傳遞，這樣函式內部直接使用原始的 msg 字串，完全避免了複製操作，速度更快、記憶體用量更少。
    // Write you code here
    for (int i = 0; i < n; i++)
    {
        std::wcout << message << std::endl;
    }
}

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    system("chcp 65001");

    // 這是最關鍵的一步：將 stdin 和 stdout 切換到 UTF-16 模式。
    // 這使得 wcin/wcout 能夠正確處理 Windows 主控台的 Unicode 輸入輸出。
    _setmode(_fileno(stdout), _O_U16TEXT);
    _setmode(_fileno(stdin), _O_U16TEXT);

    // std::string msg;
    std::wstring msg; // 使用 wstring 來儲存寬字元
    int n;

    std::wcout << L"請輸入您想重複顯示的中文訊息："; // 使用 L"" 前綴表示寬字串字面量
    std::getline(std::wcin, msg);                    // 使用 wcin 和 getline 讀取寬字串
    std::wcout << L"請輸入您想重複顯示的次數：";     // 使用 L"" 前綴表示寬字串字面量
    std::wcin >> n;                                  // 使用 wcin 讀取整數

    printNTimes(msg, n);

    system("pause"); // 按任意鍵結束
    return 0;
}
