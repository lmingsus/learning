// Recap - HashSet
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

class HashSet5

{
    public static HashSet<string> ProcessHashSet()
    {
        // Write your code here
        HashSet<string> fruits = new HashSet<string>();
        fruits.Add("Apple");
        fruits.Add("Banana");
        fruits.Add("Orange");
        Console.WriteLine($"Contains Mango: {fruits.Contains("Mango")}");
        Console.WriteLine($"Added Apple again: {fruits.Add("Apple")}");
        Console.WriteLine($"Removed Banana: {fruits.Remove("Banana")}");
        Console.WriteLine($"Count: {fruits.Count}");
        return fruits;
    }

    public void Main0()
    {
        HashSet<string> result = ProcessHashSet();

        if (result != null)
        {
            Console.WriteLine(string.Join(", ", result));
        }
    }
}