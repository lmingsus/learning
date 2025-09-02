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
Create a method called ProcessDictionary that takes a Dictionary<string, int> and an array of operations as parameters. The method should perform these operations:

1.
If the operation is "GET key", print the value for that key or "Not found" if the key doesn't exist

2.
If the operation is "CHECK key", print "Exists" if the key exists, otherwise print "Not found"

3.
If the operation is "MODIFY key value", do the following:
    If the key exists and has the same value as provided, increase its value by 1
    If the key exists but has a different value, remove the key
    If the key doesn't exist, add it with the provided value
Return the updated Dictionary after processing all operations.
*/

using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class HashMap5
{
    public static Dictionary<string, int> ProcessDictionary(Dictionary<string, int> data, string[] operations)
    {
        foreach (var operation in operations)
        {
            var parts = operation.Split(' ');
            if (parts.Length == 0) continue;

            var command = parts[0];
            var key = parts[1];
            int value;

            switch (command)
            {
                case "GET":
                    Console.WriteLine(data.TryGetValue(key, out value) ? value.ToString() : "Not found");
                    break;

                case "CHECK":
                    Console.WriteLine(data.ContainsKey(key) ? "Exists" : "Not found");
                    break;

                case "MODIFY":
                    if (parts.Length == 3 && int.TryParse(parts[2], out value))
                    {
                        if (data.ContainsKey(key))
                        {
                            if (data[key] == value)
                            {
                                data[key]++;
                            }
                            else
                            {
                                data.Remove(key);
                            }
                        }
                        else
                        {
                            data[key] = value;
                        }
                    }
                    break;
            }
        }
        return data;
    }

    public void Main0(string[] args)
    {
        // Initialize a dictionary with some data
        Dictionary<string, int> data = new Dictionary<string, int>
        {
            { "Apple", 10 },
            { "Banana", 5 },
            { "Orange", 7 }
        };

        // Sample operations
        string[] operations = new string[]
        {
            "GET Apple",
            "CHECK Mango",
            "MODIFY Banana 5",
            "MODIFY Orange 8",
            "MODIFY Mango 3"
        };

        Dictionary<string, int> result = ProcessDictionary(data, operations);

        // Display the result
        Console.WriteLine("Updated Dictionary:");
        foreach (var item in result)
        {
            Console.WriteLine($"{item.Key}: {item.Value}");
        }
    }
}