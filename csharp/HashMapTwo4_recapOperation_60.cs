// Recap - HashMap Operations
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
Create a method called ProcessDictionary that performs advanced operations on a Dictionary<string, int> inventory. The method should:

Process commands from a list of operations:
"COUNT": Print the total number of items in the inventory
"ADD item quantity": Add a new item with the specified quantity (if item exists, increment its quantity)
"REMOVE item": Remove the specified item from inventory
"UPDATE item quantity": Set the item's quantity to the specified value
"FIND item": Print the quantity of the specified item or "Not found" if it doesn't exist
For each operation, print a message in this format:
"Operation [operation] performed successfully" or
"Operation [operation] failed: [reason]"
Return the updated inventory dictionary
*/


/*

*/

using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class HashMap9
{
    public static Dictionary<string, int> ProcessDictionary(Dictionary<string, int> inventory, List<string> operations)
    {
        foreach (var operation in operations)
        {
            string[] parts = operation.Split(' ');
            string command = parts[0].ToUpper();
            // string item = operations.Count > 1 ? operations[1] : "";
            // int quantity  = operations.Count > 2 ? int.Parse(operations[2]) : 0;
            // bool sccess = true;
            // string reason = "";
            switch (command)
            {
                case "COUNT":
                    Console.WriteLine($"Total items: {inventory.Count}");
                    Console.WriteLine($"Operation {command} performed successfully");
                    break;
                case "ADD":
                    if (parts.Length == 3 && int.TryParse(parts[2], out int addQuantity))
                    {
                        string addItem = parts[1];
                        if (inventory.ContainsKey(addItem))
                        {
                            inventory[addItem] += addQuantity;
                        }
                        else
                        {
                            inventory[addItem] = addQuantity;
                        }
                        Console.WriteLine($"Operation {command} performed successfully");
                    }
                    else
                    {
                        Console.WriteLine($"Operation {command} failed: Invalid format");
                    }
                    break;
                case "REMOVE":
                    if (parts.Length == 2)
                    {
                        string removeItem = parts[1];
                        if (inventory.Remove(removeItem))
                        {
                            Console.WriteLine($"Operation {command} performed successfully");
                        }
                        else
                        {
                            Console.WriteLine($"Operation {command} failed: Item not found");
                        }
                    }
                    else
                    {
                        Console.WriteLine($"Operation {command} failed: Invalid format");
                    }
                    break;
                case "UPDATE":
                    if (parts.Length == 3 && int.TryParse(parts[2], out int updateQuantity))
                    {
                        string updateItem = parts[1];
                        if (inventory.ContainsKey(updateItem))
                        {
                            inventory[updateItem] = updateQuantity;
                            Console.WriteLine($"Operation {command} performed successfully");
                        }
                        else
                        {
                            Console.WriteLine($"Operation {command} failed: Item not found");
                        }
                    }
                    else
                    {
                        Console.WriteLine($"Operation {command} failed: Invalid format");
                    }
                    break;
                case "FIND":
                    if (parts.Length == 2)
                    {
                        string findItem = parts[1];
                        if (inventory.TryGetValue(findItem, out int hadQuantity))
                        {
                            Console.WriteLine($"{findItem}: {hadQuantity}");
                            Console.WriteLine($"Operation {command} performed successfully");
                        }
                        else
                        {
                            Console.WriteLine($"Operation {command} failed: Item not found");
                        }
                    }
                    else
                    {
                        Console.WriteLine($"Operation {command} failed: Invalid format");
                    }
                    break;
                default:
                    Console.WriteLine($"Operation {command} failed: Unknown command");
                    break;
            }
        }
        return inventory;
    }



    public void Main0(string[] args)
    {
        Dictionary<string, int> inventory = new Dictionary<string, int>();
        List<string> operations = new List<string>();

        // Read first line to check if it's JSON format for inventory
        string firstLine = Console.ReadLine();

        // Check if input is in JSON format for inventory
        if (firstLine != null && firstLine.StartsWith("{") && firstLine.EndsWith("}"))
        {
            try
            {
                // Process JSON input for inventory
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

                // Read second line for operations
                string secondLine = Console.ReadLine();

                // Check if operations are in JSON array format
                if (secondLine != null && secondLine.StartsWith("[") && secondLine.EndsWith("]"))
                {
                    try
                    {
                        // Extract content between square brackets
                        string arrayContent = secondLine.Substring(1, secondLine.Length - 2);

                        // Use regex to match all quoted strings - this is more robust
                        MatchCollection matches = Regex.Matches(arrayContent, @"""([^""]*)""");

                        foreach (Match match in matches)
                        {
                            // Add the captured group (without quotes)
                            if (match.Groups.Count > 1)
                            {
                                operations.Add(match.Groups[1].Value);
                            }
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"Error parsing operations array: {ex.Message}");
                        return;
                    }
                }
                else
                {
                    // Process operations in traditional format
                    int m = int.Parse(secondLine);
                    for (int i = 0; i < m; i++)
                    {
                        operations.Add(Console.ReadLine());
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

            // Read operations
            int m = int.Parse(Console.ReadLine());
            for (int i = 0; i < m; i++)
            {
                operations.Add(Console.ReadLine());
            }
        }

        Dictionary<string, int> result = ProcessDictionary(inventory, operations);

        // Print updated inventory
        Console.WriteLine("Final Inventory:");
        foreach (var item in result)
        {
            Console.WriteLine($"{item.Key}: {item.Value}");
        }
    }
}