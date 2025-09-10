// Recap - Validation Function

#include <iostream>
// #include <cmath>
// #include <string>
// #include <iomanip>
// using namespace std;

bool is_valid(std::string username, std::string password)
{
    // Write your code below
    // if (username == "user")
    // {
    //     if (password == "qwerty")
    //     {
    //         return true;
    //     }
    // }
    // if (username == "admin")
    //     return true;
    // return false;
    bool is_valid_user = (username == "user" && password == "qwerty");
    bool is_valid_admin = (username == "admin");
    return is_valid_user || is_valid_admin;
}

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    system("chcp 65001");

    std::string user, pass;
    std::cin >> user;
    std::cin >> pass;
    bool res = is_valid(user, pass);
    std::cout << (res ? "true" : "false");

    system("pause"); // 按任意鍵結束
    return 0;
}
