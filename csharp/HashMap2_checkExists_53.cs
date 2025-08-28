// Declare a HashMap
/*
Dictionary<string, int> fruitInventory = new Dictionary<string, int>();
fruitInventory.Add("Apple", 10);
fruitInventory.Add("Banana", 15);

initialize a Dictionary with values:
Dictionary<string, int> fruitInventory = new Dictionary<string, int>()
{
    { "Apple", 10 },
    { "Banana", 15 }
};

check if a key exists:
bool exists = fruitInventory.ContainsKey("Apple");
*/

using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class HashMap2
{
    public static void CheckKeyExists(Dictionary<string, int> dictionary, string key)
    {
        // Write code here
        if (dictionary.ContainsKey(key))
        {
            Console.WriteLine("Key exists");
        }
        else
        {
            Console.WriteLine("Key does not exist");
        }
    }

    static void Main(string[] args)
    {
        Dictionary<string, int> inventory = new Dictionary<string, int>();

        // Reading inventory input - accepts both JSON format and line-by-line format
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
                        inventory.Add(keyMatch, valueMatch);
                    }
                }

                // Reading the key to check directly
                string keyToCheck = Console.ReadLine();
                CheckKeyExists(inventory, keyToCheck);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error parsing input: {ex.Message}");
            }
        }
        else
        {
            // Process original line-by-line format
            string line = firstLine;

            // Read lines until an empty line is entered
            while (!string.IsNullOrEmpty(line))
            {
                try
                {
                    string[] parts = line.Split(':');
                    if (parts.Length == 2)
                    {
                        inventory.Add(parts[0], int.Parse(parts[1]));
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error parsing line: {ex.Message}");
                }

                // Read next line
                line = Console.ReadLine();
            }

            // Reading the key to check
            string keyToCheck = Console.ReadLine();
            CheckKeyExists(inventory, keyToCheck);
        }
    }
}