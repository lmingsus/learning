// C-style Strings Part 1

/*
C-style strings 是以 null 字元 '\0' 結尾的字元陣列 (character array)，
故也稱為 null-terminated strings。
例：
char str[] = "Hello, World!";
char str2[6] = {'W', 'o', 'r', 'l', 'd', '\0'};
char str3[10] = "Hello";  // 剩下的空間會填充 '\0'
*/

/*
宣告一個 C-style string 必須分配足夠多的空間來容納所有字元，包括另外加上一個結尾的 null 字元。
char str1[6] = "Hello";

char first = str1[0]; // 'H'
str1[0] = 'J';
*/

/*
#include <cstring>
字串操作：
strlen(str)：計算 C-style 字串的長度（不包含結尾的 \0）。
strcpy(dest, src)：（不安全） 複製一個字串到另一個。
strcat(dest, src)：（不安全） 將一個字串串接到另一個的結尾。
strcmp(str1, str2)：比較兩個字串。
strchr(str, ch)：在字串中尋找一個字元。
strstr(str1, str2)：在字串中尋找一個子字串。

記憶體操作：
memcpy(dest, src, count)：複製一塊記憶體區域。
memset(ptr, value, count)：將一塊記憶體區域的每個位元組都設定為特定值。
*/

#include <iostream>
// #include <cmath>
// #include <string> // getline
// #include <iomanip>
// #include <clocale>
#include <cstring> // 使用 strlen()
// using namespace std;

void printStringInfo(char str[])
{
    // Print the string
    std::cout << "String: " << str << std::endl;

    // Print the length of the string
    std::cout << "Length: " << strlen(str) << std::endl;

    // Print the character at index 4
    std::cout << "Character at index 4: " << str[4] << std::endl;

    // Modify the first character to 'X'
    str[0] = 'X';

    // Print the modified string
    std::cout << "Modified string: " << str << std::endl;
}

int main()
{
    // 在 cmd 上先執行「chcp 65001 命令」，將主控台的代碼頁切換為 UTF-8，以顯示正體中文
    // 這是 Windows 特有的指令。
    system("chcp 65001 >> nul");

    char str3[10] = "Hello";
    std::cout << str3 << std::endl;
    for (size_t i = 0; i < sizeof(str3); i++)
    {
        std::cout << str3[i] << ", ";
    }
    std::cout << "結束" << std::endl;
    // H, e, l, l, o, , , , , , 結束

    char message[] = "Hello, World!";

    printStringInfo(message);

    system("pause"); // 按任意鍵結束
    return 0;
}
