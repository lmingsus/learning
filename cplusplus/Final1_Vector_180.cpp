// Vector Data Filtering

/*
std::vector<int> filterNumbers(std::vector<int> numbers) {
    std::vector<int> result;
    for (int num : numbers) {
        if (num > 10) {
            result.push_back(num);
        }
    }
    return result;
}
*/

#include <iostream>
// #include <cmath>
// #include <string> // std::string, std::stoi, std::getline
// #include <iomanip> // For std::fixed and std::setprecision
// #include <clocale>
// #include <cstring> // 使用 strlen()
#include <vector>
// #include <map>
// #include <set>
// #include <vector>
// #include <algorithm> // std::sort
// #include <stdexcept> // std::invalid_argument
// using namespace std;

// TODO: Create the filterNumbers function here
// 參數改為 const reference (const &)，避免複製整個 vector，提升效能。
std::vector<int> filterNumbers(const std::vector<int> &numbers, int threshold)
{
    std::vector<int> result;
    // 對於 int 這種基本型別，直接傳值 (pass-by-value) 最清晰且高效。
    for (int num : numbers)
        if (num > threshold)
            result.push_back(num);
    return result;
}

int main()
{
    // Read the number of integers
    int n;
    std::cin >> n;

    // Read the integers into a vector
    // 預先分配 vector 大小，避免迴圈中不必要的重新分配記憶體。
    std::vector<int> numbers(n);
    for (int &num : numbers)
        std::cin >> num;

    // Read the threshold
    int threshold;
    std::cin >> threshold;

    // TODO: Call the filterNumbers function and store the result
    std::vector<int> result = filterNumbers(numbers, threshold);
    // TODO: Print the filtered count and numbers according to the required format
    std::cout << "Filtered count: " << result.size() << std::endl;
    if (!result.empty())
        for (int num : result)
            std::cout << num << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}