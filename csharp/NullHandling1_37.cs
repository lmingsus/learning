// Null Reference Basics
/*
Create a method called ProcessName that takes a string parameter called name. The method should:

Check if the name is null
If the name is null, print: "Name is null"
If the name is not null, print: "Name length is X" (where X is the length of the name)
*/
using System;
using System.IO;

class NullHandling1
{
    public static void ProcessName(string? name)
    {
        // Write your code here
        if (name == null)
        {
            Console.WriteLine("Name is null");
        }
        else
        {
            Console.WriteLine("Name length is " + name.Length);
        }
    }

    public void Main0()
    {
        string input = Console.ReadLine() ?? "null";

        // Convert "null" string to actual null
        string? name = input.ToLower() == "null" ? null : input;

        ProcessName(name);
    }
}
