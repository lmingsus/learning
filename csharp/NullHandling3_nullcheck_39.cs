// Null Reference Basics
/*
if (name == null)
{
    Console.WriteLine("Name is null");
}

string name = null;
int? length = name?.Length;  // length will be null

string name = null;
string displayName = name ?? "Unknown";  // displayName will be "Unknown"

string name = null;
int length = (name ?? "").Length;  // length will be 0
*/

/*
Create a method called processUserName that takes a string parameter userName. The method should:

If userName is null, return "No user provided"
If userName is empty or only whitespace, return "Invalid username"
Otherwise, return "Welcome, [userName]!" where [userName] is the actual username
Remember to use appropriate null checking patterns.
*/
using System;
using System.IO;

class NullHandling3
{
    public static string processUserName(string userName)
    {
        // Write your code here
        if (userName == null)
        {
            return "No user provided";
        }
        else if (String.IsNullOrWhiteSpace(userName))
        {
            return "Invalid username";
        }
        else
        {
            return $"Welcome, {userName}!";
        }
    }
}
