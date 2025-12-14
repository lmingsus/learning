// Map Value Search

/*
std::vector<std::string> findKeysWithValue(std::map<std::string, int> data, int target) {
    std::vector<std::string> matches;
    for (auto pair : data) {
        if (pair.second == target) {
            matches.push_back(pair.first);
        }
    }
    return matches;
}
*/

#include <iostream>
// #include <cmath>
// #include <string> // std::string, std::stoi, std::getline
// #include <iomanip> // For std::fixed and std::setprecision
// #include <clocale>
// #include <cstring> // 使用 strlen()
#include <vector>
#include <map>
// #include <set>
// #include <algorithm> // std::sort
// #include <stdexcept> // std::invalid_argument
// using namespace std;

std::vector<std::string> findKeysWithValue(const std::map<std::string, int> &map, int targetValue)
{
    std::vector<std::string> result;
    for (const auto &entry : map)
        if (entry.second == targetValue)
            result.push_back(entry.first);
    return result;
}

int main()
{
    // Read number of key-value pairs
    int n;
    std::cin >> n;

    // Create map to store key-value pairs
    std::map<std::string, int> keyValueMap;

    // Read n key-value pairs
    for (int i = 0; i < n; i++)
    {
        std::string key;
        int value;
        std::cin >> key >> value;
        keyValueMap[key] = value;
    }

    // Read target value to search for
    int targetValue;
    std::cin >> targetValue;

    // TODO: Call your findKeysWithValue function and store the result
    std::vector<std::string> result = findKeysWithValue(keyValueMap, targetValue);
    // TODO: Print the results in the required format
    // First print "Keys found: [count]"
    // Then print each matching key on separate lines
    std::cout << "Keys found: " << result.size() << std::endl;
    // 這個 if (!result.empty()) 檢查不是必要的，因為範圍-based for 迴圈
    // 在處理一個空容器時，本來就不會執行任何疊代。移除它可以讓程式碼更簡潔。
    for (const std::string &ele : result)
        std::cout << ele << std::endl;

    system("pause"); // 按任意鍵結束
    return 0;
}