// Checking if an Element Exists
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
*/


/*

*/


/*

*/

using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class HashSet3
{
    public static string ElementExists(HashSet<string> set, string element)
    {
        // Write your code here
        if (set.Contains(element))
        {
            return $"The element '{element}' exists in the set";
        }
        else
        {
            return $"The element '{element}' does not exist in the set";
        }
    }

    public void Main0()
    {
        // Read first line to check if it's JSON format
        string firstLine = Console.ReadLine();
        string elementToCheck = Console.ReadLine();
        HashSet<string> set = new HashSet<string>();

        // Check if input is in JSON array format
        if (firstLine != null && firstLine.StartsWith("[") && firstLine.EndsWith("]"))
        {
            try
            {
                // Extract content between square brackets
                string arrayContent = firstLine.Substring(1, firstLine.Length - 2);

                // Use regex to match all quoted strings
                MatchCollection matches = Regex.Matches(arrayContent, @"""([^""]*)""");

                foreach (Match match in matches)
                {
                    // Add the captured group (without quotes)
                    if (match.Groups.Count > 1)
                    {
                        set.Add(match.Groups[1].Value.Trim());
                    }
                }

                // Check if element is in JSON string format
                Match elementMatch = Regex.Match(elementToCheck, @"""([^""]*)""");
                if (elementMatch.Success && elementMatch.Groups.Count > 1)
                {
                    elementToCheck = elementMatch.Groups[1].Value;
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
            // Process traditional comma-separated input
            string[] elements = firstLine.Split(',');
            foreach (string element in elements)
            {
                set.Add(element.Trim());
            }
        }

        string result = ElementExists(set, elementToCheck);
        Console.WriteLine(result);
    }
}