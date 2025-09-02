// Recap - Manage Warehouse
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
ManageWarehouse method that performs the following operations:

First, print all items and their quantities in format: "Item: [item], Quantity: [quantity]"
Check if "apples" exist in inventory and print: "Apples in stock: [True/False]"
Add 10 to the quantity of "bananas" if they exist (use direct value modification)
Remove any item that has 0 quantity
Print the total number of distinct items in the warehouse
Finally, return the updated inventory dictionary
*/


/*

*/

using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class HashMap8
{
    public static Dictionary<string, int> ManageWarehouse(Dictionary<string, int> inventory)
    {
        // Print all items and their quantities
        foreach (var item in inventory)
        {
            Console.WriteLine($"Item: {item.Key}, Quantity: {item.Value}");
        }

        // Check if "apples" exist in inventory
        bool applesExist = inventory.ContainsKey("apples");
        Console.WriteLine($"Apples in stock: {applesExist}");

        // Add 10 to the quantity of "bananas" if they exist
        // if (inventory.TryGetValue("bananas", out int bananaValue))
        // {
        //     inventory["bananas"] = bananaValue + 10;
        // }
        if (inventory.ContainsKey("bananas"))
        {
            inventory["bananas"] += 10;
        }

        // Remove any item that has 0 quantity
        // int removeCount = 0;
        // string[] removeKeys = new string[inventory.Count];
        // foreach (var item in inventory)
        // {
        //     if (item.Value == 0)
        //     {
        //         removeKeys[removeCount] = item.Key;
        //         removeCount++;
        //     }
        // }
        // for (int k = 0; k < removeCount; k++)
        // {
        //     inventory.Remove(removeKeys[k]);
        // }
        var itemsToRemove = new List<string>();
        foreach (var item in inventory)
        {
            if (item.Value == 0)
            {
                itemsToRemove.Add(item.Key);
            }
        }
        foreach (var item in itemsToRemove)
        {
            inventory.Remove(item);
        }

        // Print the total number of distinct items
        Console.WriteLine($"Total distinct items: {inventory.Count}");

        return inventory;
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
            int n = int.Parse(firstLine);
            for (int i = 0; i < n; i++)
            {
                string[] parts = Console.ReadLine().Split(':');
                inventory.Add(parts[0], int.Parse(parts[1]));
            }
        }

        Dictionary<string, int> result = ManageWarehouse(inventory);

        // Print updated inventory
        Console.WriteLine("Updated Inventory:");
        foreach (var item in result)
        {
            Console.WriteLine($"{item.Key}: {item.Value}");
        }
    }
}