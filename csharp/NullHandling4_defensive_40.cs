// Defensive Programming
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
Create a method named ProcessUserData that accepts a string parameter userData. The method should:

Check if userData is null - if it is, print "Error: User data is null" and return.
Check if userData is empty - if it is, print "Error: User data is empty" and return.
If the data is valid, convert it to uppercase and print "Processing: [UPPERCASE_DATA]".
*/
using System;

class NullHandling4
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
