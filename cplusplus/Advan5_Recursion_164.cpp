// Introduction to Recursion
// Recursive Factorial

/*
int factorial(int n) {
    if (n <= 1) {           // Base case: 0! and 1! both equal 1
        return 1;
    }

    return n * factorial(n - 1);  // Recursive step: n! = n × (n-1)!
}
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
using namespace std;

// Function must be defined outside of main() in standard C++.
int factorial(int n)
{
    // Base case: 0! and 1! are both 1.
    if (n <= 1)
        return 1;

    // Recursive step
    return n * factorial(n - 1);
}

int main()
{
    // Read input
    int n;
    cin >> n;

    // Call the factorial function and store the result
    int result = factorial(n);
    // Output the result
    cout << "Factorial of " << n << " is " << result << endl;

    system("pause"); // 按任意鍵結束
    return 0;
}