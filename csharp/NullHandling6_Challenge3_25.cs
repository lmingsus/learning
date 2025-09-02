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
Create a method named validateUserInput that accepts three parameters:

A string username
A string email
An integer age
The method should:

Check if any parameter is invalid:
Check if username is null or empty
Check if email is null or doesn't contain "@" character
Check if age is less than 18
If any validation fails, print the appropriate error message:
"ERROR: Invalid username" for null/empty username
"ERROR: Invalid email format" for null/invalid email
"ERROR: User must be 18 or older" for invalid age
If all validations pass, print "User data validated successfully"
*/
using System;

class NullHandling6
{
    public static void validateUserInput(string username, string email, int age)
    {
        // Write your code here
        if (string.IsNullOrWhiteSpace(username))
        {
            Console.WriteLine("ERROR: Invalid username");
            return;
        }
        if (string.IsNullOrWhiteSpace(email) || !email.Contains("@"))
        {
            Console.WriteLine("ERROR: Invalid email format");
            return;
        }
        if (age < 18)
        {
            Console.WriteLine("ERROR: User must be 18 or older");
            return;
        }
        Console.WriteLine("User data validated successfully");
    }
}