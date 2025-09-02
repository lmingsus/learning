// Math - Symmetric Difference
/*
HashSet<string> fruits = new HashSet<string>();
fruits.Add("Apple");
fruits.Add("Banana");
fruits.Add("Cherry");

fruits.Add("Apple"); // Returns false, element already exists
{ "Apple", "Banana", "Cherry" }

bool wasRemoved = fruits.Remove("Banana");

bool hasApple = fruits.Contains("Apple");  // Returns true
bool hasOrange = fruits.Contains("Orange"); // Returns false
bool hasOrange = fruits.Contains("Orange"); // Returns false

int size = fruits.Count;

bool hasElements = fruits.Any();  // true since the set contains elements

*/

/*
HashSet<int> set1 = new HashSet<int>() { 1, 2, 3 };
HashSet<int> set2 = new HashSet<int>() { 3, 4, 5 };

HashSet<int> unionSet = new HashSet<int>(set1);
unionSet.UnionWith(set2);

set1.IntersectWith(set2); // set1 now contains { 3 }

HashSet<int> intersection = new HashSet<int>(set1); // create a copy first
intersection.IntersectWith(set2);

HashSet<string> difference = new HashSet<string>(set1);
difference.ExceptWith(set2);

HashSet<int> symmetricDifference = new HashSet<int>(set1);
symmetricDifference.SymmetricExceptWith(set2);  // symmetric difference: { 1, 2, 4, 5 }
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

class HashSetTwo4
{
    public static HashSet<int> FindSymmetricDifference(HashSet<int> set1, HashSet<int> set2)
    {
        // Write your code here
        set1.SymmetricExceptWith(set2);
        return set1;
    }

    public void Main0()
    {
        string[] input1 = Console.ReadLine().Split(',');
        string[] input2 = Console.ReadLine().Split(',');

        HashSet<int> set1 = new HashSet<int>();
        HashSet<int> set2 = new HashSet<int>();

        foreach (string s in input1)
        {
            if (int.TryParse(s.Trim(), out int num))
            {
                set1.Add(num);
            }
        }

        foreach (string s in input2)
        {
            if (int.TryParse(s.Trim(), out int num))
            {
                set2.Add(num);
            }
        }

        HashSet<int> result = FindSymmetricDifference(set1, set2);

        // Print the result in ascending order
        int[] orderedResult = result.OrderBy(x => x).ToArray();
        foreach (int num in orderedResult)
        {
            Console.WriteLine(num);
        }
    }
}