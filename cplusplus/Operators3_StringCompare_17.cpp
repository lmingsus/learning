/*
string str1 = "hello";
string str2 = "hello";
string str3 = "Hello";

bool result1 = (str1 == str2);  // true
bool result2 = (str1 == str3);  // false (case-sensitive)
bool result3 = (str1 != str3);  // true

*/

/*


*/

#include <iostream>
#include <cmath>
#include <string>
using namespace std;

int main()
{
    string str1 = "a";
    string str2 = "b";
    string str3 = "c";

    cout << str2.compare(str1) << endl;
    // Positive (b comes after a)

    cout << str2.compare(str3) << endl;
    // Negative (b comes before c)

    cout << str2.compare(str2) << endl;
    // 0 (equal strings)

    str1 = "programming";
    str2 = "Programming";

    cout << str2 << ".compare(" << str1 << "): " << str2.compare(str1) << endl;
    // Negative (P comes before p)

    system("pause"); // 按任意鍵結束
    return 0;
}