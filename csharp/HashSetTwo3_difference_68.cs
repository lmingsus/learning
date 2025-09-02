// Math - Set Difference
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
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

class HashSetTwo3
{
    public static HashSet<int> GetSetDifference(HashSet<int> set1, HashSet<int> set2)
    {
        // Write your code here
        set1.ExceptWith(set2);
        return set1;
    }

    public void Main0()
    {
        // Read first line for first set
        string line1 = Console.ReadLine();
        HashSet<int> set1 = new HashSet<int>();

        // Check if first set is in JSON array format
        if (line1 != null && line1.StartsWith("[") && line1.EndsWith("]"))
        {
            try
            {
                // Extract content between square brackets
                string arrayContent = line1.Substring(1, line1.Length - 2);

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
                        set1.Add(num);
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error parsing first set: {ex.Message}");
                return;
            }
        }
        else
        {
            // Process traditional space-separated input for first set
            string[] set1Input = line1.Split(' ');
            foreach (string item in set1Input)
            {
                if (int.TryParse(item, out int num))
                {
                    set1.Add(num);
                }
            }
        }

        // Read second line for second set
        string line2 = Console.ReadLine();
        HashSet<int> set2 = new HashSet<int>();

        // Check if second set is in JSON array format
        if (line2 != null && line2.StartsWith("[") && line2.EndsWith("]"))
        {
            try
            {
                // Extract content between square brackets
                string arrayContent = line2.Substring(1, line2.Length - 2);

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
                        set2.Add(num);
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error parsing second set: {ex.Message}");
                return;
            }
        }
        else
        {
            // Process traditional space-separated input for second set
            string[] set2Input = line2.Split(' ');
            foreach (string item in set2Input)
            {
                if (int.TryParse(item, out int num))
                {
                    set2.Add(num);
                }
            }
        }

        HashSet<int> difference = GetSetDifference(set1, set2);

        // Print result
        List<int> sortedResult = new List<int>(difference);
        sortedResult.Sort();
        foreach (int item in sortedResult)
        {
            Console.WriteLine(item);
        }
    }
}