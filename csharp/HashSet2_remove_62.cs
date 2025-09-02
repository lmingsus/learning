// Removing an Element
/*
HashSet<string> fruits = new HashSet<string>();
fruits.Add("Apple");
fruits.Add("Banana");
fruits.Add("Cherry");

fruits.Add("Apple"); // Returns false, element already exists
{ "Apple", "Banana", "Cherry" }

bool wasRemoved = fruits.Remove("Banana");
*/


/*

*/


/*

*/

using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class HashSet2
{
    public static void RemoveElement(HashSet<string> set, string element)
    {
        // Write your code here
        bool wasRemoved = set.Remove(element);
        Console.WriteLine($"Element removed: {wasRemoved}");
        Console.WriteLine(String.Join(", ", set));
    }

    public void Main0()
    {
        HashSet<string> set = new HashSet<string>();

        // Read first line to check if it's JSON format
        string firstLine = Console.ReadLine();
        string elementToRemove;

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

                // Read second line for element to remove
                string secondLine = Console.ReadLine();

                // Check if element is in JSON string format
                Match elementMatch = Regex.Match(secondLine, @"""([^""]*)""");
                if (elementMatch.Success && elementMatch.Groups.Count > 1)
                {
                    elementToRemove = elementMatch.Groups[1].Value;
                }
                else
                {
                    elementToRemove = secondLine;
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
            // Process traditional input format
            string[] elements = firstLine.Split(',');
            foreach (string element in elements)
            {
                set.Add(element.Trim());
            }

            // Read element to remove in traditional format
            elementToRemove = Console.ReadLine();
        }

        RemoveElement(set, elementToRemove);
    }
}