// Adding an Element
/*
HashSet<string> fruits = new HashSet<string>();
fruits.Add("Apple");
fruits.Add("Banana");
fruits.Add("Cherry");

fruits.Add("Apple"); // Returns false, element already exists
{ "Apple", "Banana", "Cherry" }
*/


/*

*/


/*

*/

using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class HashSet1
{
    public static void AddElement(HashSet<string> set, string element)
    {
        // Write your code here
        set.Add(element);
        Console.WriteLine("{" + string.Join(", ", set) + "}");
    }

    public void Main0()
    {
        string[] initialElements = Console.ReadLine().Split(',') ?? Array.Empty<string>();
        string elementToAdd = Console.ReadLine() ?? string.Empty;

        HashSet<string> set = new HashSet<string>();
        foreach (string item in initialElements)
        {
            if (!string.IsNullOrWhiteSpace(item))
            {
                set.Add(item.Trim(new char[] { '[', ']', '"' }));
            }
        }

        AddElement(set, elementToAdd);
    }
}