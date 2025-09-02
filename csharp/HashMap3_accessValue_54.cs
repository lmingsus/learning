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

Accessing a value using a key:
int appleCount = fruitInventory["Apple"];
int bananaCount = fruitInventory["Banana"];

Be careful! If you try to access a key that doesn't exist, you'll get a KeyNotFoundException.
*/

using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class HashMap3
{
    public static void GetValueByKey(Dictionary<string, int> dictionary, string key)
    {
        // Write code here
        if (dictionary.ContainsKey(key))
        {
            Console.WriteLine(dictionary[key]);
        }
        else
        {
            Console.WriteLine("Key not found");
        }
    }

    static void Main0(string[] args)
    {
        // Read in a dictionary in JSON format: {"key1":value1,"key2":value2}
        string dictionaryInput = Console.ReadLine();
        string key = Console.ReadLine();

        Dictionary<string, int> dictionary = new Dictionary<string, int>();

        // Parse the input string to create a dictionary
        if (!string.IsNullOrEmpty(dictionaryInput))
        {
            try
            {
                // Check if input is in JSON format
                if (dictionaryInput.StartsWith("{") && dictionaryInput.EndsWith("}"))
                {
                    // Remove the curly braces
                    string jsonContent = dictionaryInput.Substring(1, dictionaryInput.Length - 2);

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
                            dictionary.Add(keyMatch, valueMatch);
                        }
                    }
                }
                // Handle the original format "key1:value1,key2:value2" as fallback
                else
                {
                    string[] pairs = dictionaryInput.Split(',');
                    foreach (string pair in pairs)
                    {
                        string[] keyValue = pair.Split(':');
                        if (keyValue.Length == 2)
                        {
                            dictionary.Add(keyValue[0], int.Parse(keyValue[1]));
                        }
                    }
                }

                GetValueByKey(dictionary, key);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error parsing input: {ex.Message}");
            }
        }
    }
}