// Declare a HashMap
/*
Dictionary<string, int> fruitInventory = new Dictionary<string, int>();
fruitInventory.Add("Apple", 10);
fruitInventory.Add("Banana", 15);


Dictionary<string, int> fruitInventory = new Dictionary<string, int>()
{
    { "Apple", 10 },
    { "Banana", 15 }
};

bool exists = fruitInventory.ContainsKey("Apple");

int appleCount = fruitInventory["Apple"];  // key that doesn't exist, you'll get a KeyNotFoundException.

Update an existing key's value:
if (inventory.ContainsKey("apple"))
{
    inventory["apple"] = 15;  // Updates "apple" to have value 15
}

Remove a key-value pair:
inventory.Remove("apple");
inventory.Remove("orange");    // It returns false and doesn't modify the dictionary:

Clear all entries: Remove all key-value pairs
inventory.Clear();

Get all keys
Dictionary<string, int>.KeyCollection keys = inventory.Keys;
foreach (string name in keys)
{
    Console.WriteLine(name);
}

Get all values
Dictionary<string, int>.ValueCollection values = inventory.Values;
foreach (int value in values)
{
    Console.WriteLine(value);
}
*/

/*
Create a method named ProcessDictionary that takes a Dictionary<string, int> as an argument and performs the following operations:

1.
Print "Keys: " followed by all keys (one per line)

2.
Print "Values: " followed by all values (one per line)

3.
Check if the dictionary contains the key "total" and print "Contains 'total': True" or "Contains 'total': False"

4.
Remove the key "temp" if it exists

5.
Print the count of items in the dictionary after these operations
*/

using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class HashMap6
{
    static void ProcessDictionary(Dictionary<string, int> dict)
    {
        Console.WriteLine("Keys:");
        foreach (var key in dict.Keys)
        {
            Console.WriteLine(key);
        }

        Console.WriteLine("Values:");
        foreach (var value in dict.Values)
        {
            Console.WriteLine(value);
        }

        Console.WriteLine($"Contains 'total': {dict.ContainsKey("total")}");
        dict.Remove("temp");
        Console.WriteLine($"Count after operations: {dict.Count}");
    }


    static void Main(string[] args)
    {
        Dictionary<string, int> inputDict = new Dictionary<string, int>();

        // Read first line to check if it's JSON format
        string firstLine = Console.ReadLine();

        // Check if input is in JSON format
        if (firstLine != null && firstLine.StartsWith("{") && firstLine.EndsWith("}"))
        {
            try
            {
                // Process JSON input
                string jsonContent = firstLine.Substring(1, firstLine.Length - 2);

                // Split by commas that are not inside quotes
                string pattern = @",(?=(?:[^""]*""[^""]*"")*[^""]*$)";
                string[] entries = Regex.Split(jsonContent, pattern);

                foreach (string entry in entries)
                {
                    // Extract key and value using regex
                    Match match = Regex.Match(entry, @"""([^""]+)""\s*:\s*(\d+)");
                    if (match.Success)
                    {
                        string keyMatch = match.Groups[1].Value;
                        int valueMatch = int.Parse(match.Groups[2].Value);
                        inputDict.Add(keyMatch, valueMatch);
                    }
                }

                ProcessDictionary(inputDict);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error parsing input: {ex.Message}");
            }
        }
        else
        {
            try
            {
                // Process traditional input format
                int n = int.Parse(firstLine);

                for (int i = 0; i < n; i++)
                {
                    string[] pair = Console.ReadLine().Split(':');
                    string key = pair[0];
                    int value = int.Parse(pair[1]);
                    inputDict.Add(key, value);
                }

                ProcessDictionary(inputDict);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error parsing input: {ex.Message}");
            }
        }
    }
}