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

Update an existing key's value:
if (inventory.ContainsKey("apple"))
{
    inventory["apple"] = 15;  // Updates "apple" to have value 15
}

Remove a key-value pair:
inventory.Remove("apple");
It returns false and doesn't modify the dictionary:
inventory.Remove("orange");

Clear all entries: Remove all key-value pairs
inventory.Clear();
*/

/*
Create a method named UpdateInventory that takes three arguments:

A Dictionary<string, int> representing an inventory
A string representing an item name
An int representing the new quantity
The method should:

If the item exists in the inventory, update its quantity
If the item doesn't exist, add it with the given quantity
Print the updated inventory in the format: "Item: [quantity]" (one item per line)
*/

using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class HashMap4
{
    public static void UpdateInventory(Dictionary<string, int> inventory, string item, int quantity)
    {
        // Write your code here
        if (inventory.ContainsKey(item))
        {
            inventory[item] = quantity;
        }
        else
        {
            inventory.Add(item, quantity);
        }

        // foreach (var entry in inventory)
        // {
        //     Console.WriteLine($"Item: {entry.Key}, Quantity: {entry.Value}");
        // }
        foreach (KeyValuePair<string, int> entry in inventory)
        {
            Console.WriteLine($"{entry.Key}: {entry.Value}");
        }
    }

    public void Main0(string[] args)
    {
        Dictionary<string, int> inventory = new Dictionary<string, int>();

        // Read first line to check if it's JSON format
        string firstLine = Console.ReadLine();

        // Check if input is in JSON format
        if (firstLine != null && firstLine.StartsWith("{") && firstLine.EndsWith("}"))
        {
            try
            {
                // Process JSON input for initial inventory
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

                // Read the item to update and its quantity
                string updateItemJson = Console.ReadLine();
                // Check if update item is in JSON format with quotes
                Match itemMatch = Regex.Match(updateItemJson, @"""([^""]+)""");
                string updateItem = itemMatch.Success ? itemMatch.Groups[1].Value : updateItemJson;

                int updateQuantity = int.Parse(Console.ReadLine());

                UpdateInventory(inventory, updateItem, updateQuantity);
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
                int initialCount = int.Parse(firstLine);
                for (int i = 0; i < initialCount; i++)
                {
                    string item = Console.ReadLine();
                    int quantity = int.Parse(Console.ReadLine());
                    inventory.Add(item, quantity);
                }

                // Read the item to update and its quantity
                string updateItem = Console.ReadLine();
                int updateQuantity = int.Parse(Console.ReadLine());

                UpdateInventory(inventory, updateItem, updateQuantity);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error parsing input: {ex.Message}");
            }
        }
    }
}