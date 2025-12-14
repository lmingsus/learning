// Create Set & Add Elements

/*
std::set<int> numbers;
numbers.insert(5);
numbers.insert(2);
numbers.insert(8);
*/

#include <iostream>
// #include <cmath>
// #include <string> // getline
// #include <iomanip> // For std::fixed and std::setprecision
// #include <clocale>
// #include <cstring> // 使用 strlen()
// #include <vector>
// #include <map>
#include <set>
using namespace std;

int main()
{
    // Read the number of integers to insert
    int n;
    cin >> n;

    // Create an empty set
    set<int> mySet;

    // TODO: Write your code here
    // Use a loop to read n integers and insert them into the set
    // Calculate how many duplicates were ignored
    for (int i = 0; i < n; i++)
    {
        int input;
        cin >> input;
        mySet.insert(input);
    }

    // Output the results
    cout << "Set size: " << mySet.size() << endl;
    cout << "Duplicates ignored: " << (n - mySet.size()) << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}