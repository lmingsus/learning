// Iterating Over Sets
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

foreach (string fruit in fruits)
{
    Console.WriteLine(fruit);
}

doesn't maintain insertion order:
string[] fruitsArray = fruits.ToArray();

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
using System.Text.RegularExpressions;

class HashSetTwo5
{
    public static void PrintSetElements(HashSet<int> set)
    {
        // Write your code here
    }

    public void Main0()
    {
        HashSet<int> numbers = new HashSet<int>();

        // Read first line to check format
        string firstLine = Console.ReadLine() ?? "";

        // Check if input is in JSON array format
        if (firstLine != null && firstLine.StartsWith("[") && firstLine.EndsWith("]"))
        {
            try
            {
                // Extract content between square brackets
                string arrayContent = firstLine.Substring(1, firstLine.Length - 2);

                // Try to parse the JSON array content
                string[] values = Regex.Split(arrayContent, @",\s*");
                foreach (string value in values)
                {
                    // Remove any quotes if present
                    string cleanValue = value.Trim();
                    if (cleanValue.StartsWith("\"") && cleanValue.EndsWith("\""))
                    {
                        cleanValue = cleanValue.Substring(1, cleanValue.Length - 2);
                    }

                    // Parse as integer and add to set
                    if (int.TryParse(cleanValue, out int num))
                    {
                        numbers.Add(num);
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error parsing JSON input: {ex.Message}");
                return;
            }
        }
        else
        {
            try
            {
                // Traditional format - read count then elements
                int count = int.Parse(firstLine);

                // Read each element and add to the set
                for (int i = 0; i < count; i++)
                {
                    int num = int.Parse(Console.ReadLine());
                    numbers.Add(num);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error parsing traditional input: {ex.Message}");
                return;
            }
        }

        PrintSetElements(numbers);
    }
}
