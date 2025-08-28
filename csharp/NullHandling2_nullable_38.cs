// Null Reference Basics
/*
Create a method called ProcessName that takes a string parameter called name. The method should:

Check if the name is null
If the name is null, print: "Name is null"
If the name is not null, print: "Name length is X" (where X is the length of the name)s
*/
using System;
using System.IO;

class NullHandling2
{
    // Implement the ProcessNullableAge method here
    static int ProcessNullableAge(int? age)
    {
        if (age.HasValue)
        {
            Console.WriteLine($"Age is: {age} years");
            return (int)age;
        }
        else
        {
            Console.WriteLine("Age not provided");
            return 0;
        }

    }

    static void Main(string[] args)
    {
        string input = Console.ReadLine() ?? "null";

        int? age = null;
        if (input != "null")
        {
            age = int.Parse(input);
        }

        int result = ProcessNullableAge(age);
        Console.WriteLine("Returned value: " + result);
    }
}
