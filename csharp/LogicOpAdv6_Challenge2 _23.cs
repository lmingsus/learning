// Conditional Logical Operators
/*


*/

/*
Create a program that safely processes a list of potentially null values. You need to:

Create a method named ProcessNames that takes an array of strings (names)
For each name in the array, print "[Name] is present" if the name is not null
If a name is null, print "Unknown guest is present" instead
Use the null-coalescing operator (??) in your solution
*/
using System;

class LogicOpAdv6
{
    public static void processNames(string[] names)
    {
        // Write your solution here
        foreach (string name in names)
        {
            Console.WriteLine($"{name ?? "Unknown guest"} is present");
        }
    }

}
