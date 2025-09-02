// Empty and Size
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

using System;
using System.Collections.Generic;
using System.Linq;

class HashSet4
{
    public static void CountAndCheck(HashSet<string> set)
    {
        // Write your code here
        if (!set.Any())
        {
            Console.WriteLine("Empty set");
        }
        else
        {
            Console.WriteLine($"Set contains {set.Count} elements");
        }
    }

    public void Main0()
    {
        // Read input for HashSet elements separated by commas
        // If the input is empty, create an empty HashSet
        string input = Console.ReadLine();

        HashSet<string> set = new HashSet<string>();
        if (!string.IsNullOrEmpty(input))
        {
            string[] elements = input.Split(',');
            foreach (string element in elements)
            {
                set.Add(element.Trim());
            }
        }

        CountAndCheck(set);
    }
}