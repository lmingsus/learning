// Recap - Lambda Sort

/*
#include <algorithm>
std::sort 是 C++ 標準庫中的一個函數，用於對容器中的元素進行排序。
它可以接受一個比較函數作為參數，這個比較函數定義了排序的規則。

`std::sort` 是 C++ 標準庫 `<algorithm>` 中的一個強大函數，用於對容器中的元素進行排序。
當需要自訂排序規則時，可以傳入第三個參數：一個比較函式。
*/

/*
std::vector<int> numbers = {5, 2, 8, 1, 9};
對整個 vector 進行排序
std::sort(numbers.begin(), numbers.end()); // 默認為升序排序
*/

/*
當您需要對複雜的物件（例如 struct 或 class）進行排序，
或者您不想要預設的升序排序時，您可以傳入第三個參數——一個比較函式。
std::vector<Student> students = {
    {"Alice", 85},
    {"Bob", 92},
    {"Carol", 78},
    {"David", 92}
};

使用 Lambda 作為比較函式，傳參考以避免不必要的
std::sort(students.begin(), students.end(),
    這個 Lambda 告訴 sort 如何比較兩個學生 a 和 b
    [](const Student& a, const Student& b) {
        如果 a 的分數大於 b 的分數，那麼 a 應該排在 b 的前面
        return a.score > b.score;
    }
);
*/

#include <iostream>
// #include <cmath>
// #include <string> // getline
// #include <iomanip> // For std::fixed and std::setprecision
// #include <clocale>
// #include <cstring> // 使用 strlen()
// #include <vector>
// #include <map>
// #include <set>
#include <vector>
#include <algorithm> // std::sort
// using namespace std;

int main()
{
    // Read input
    int n;
    std::cin >> n;

    std::vector<int> numbers(n);
    for (int i = 0; i < n; i++)
    {
        std::cin >> numbers[i];
    }

    char order;
    std::cin >> order;

    // TODO: Write your code below
    // Use std::sort with a lambda expression to sort the vector
    // based on the order character (A for ascending, D for descending)
    if (order == 'A')
    {
        std::sort(numbers.begin(), numbers.end(), [](int a, int b)
                  { return a < b; });
    }
    else if (order == 'D')
    {
        std::sort(numbers.begin(), numbers.end(), [](int a, int b)
                  { return a > b; });
    }
    // Output the sorted elements
    for (int num : numbers)
    {
        std::cout << num << std::endl;
    }

    system("pause"); // 按任意鍵結束
    return 0;
}