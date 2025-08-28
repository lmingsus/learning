// Recap - Null Safety
/*
Instead of:
string city = null;
if (customer != null && customer.Address != null)
{
    city = customer.Address.City;
}

Use this:
string city = customer?.Address?.City;
*/

/*
Create a method called SafelyProcessData that takes two parameters:

A string name that could be null
A nullable int age
The method should:

Check if name is null or empty using appropriate null checking patterns
Check if age has a value
Return a formatted string as follows:
If name is null, return "No name provided"
If name is empty or whitespace, return "Invalid name"
If age is null, return "Name: [name], Age: Unknown"
Otherwise, return "Name: [name], Age: [age]"
Make sure to use defensive programming techniques to handle all possible null scenarios!
*/
using System;

class NullHandling5
{
    public static void processUserData(string userData)
    {
        // Write your code here
        if (userData == null)
        {
            Console.WriteLine("Error: User data is null");
            return;
        }
        else if (userData.Length == 0)
        {
            Console.WriteLine("Error: User data is empty");
            return;
        }
        else
        {
            string upperData = userData.ToUpper();
            Console.WriteLine("Processing: " + upperData);
        }
    }
}
