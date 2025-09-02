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
*/

using System;
using System.Collections.Generic;

class HashMap1
{
    public static Dictionary<string, int> CreateFruitInventory()
    {
        // Write your code here
        Dictionary<string, int> fruitInventory = new Dictionary<string, int>()
        {
            { "Apple", 5 },
            { "Banana", 10 },
            { "Orange", 7 },
        };
        return fruitInventory;
    }

    public void Main0(string[] args)
    {
        Dictionary<string, int> inventory = CreateFruitInventory();

        // Display the inventory
        foreach (var item in inventory)
        {
            Console.WriteLine($"{item.Key}: {item.Value}");
        }
    }
}