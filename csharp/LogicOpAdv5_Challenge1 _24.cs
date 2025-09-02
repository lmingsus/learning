// Short-Circuit Evaluation
/*
Create a method named safeDataAccess that takes two parameters:

A string array data
An integer index
The method should check:

If data is not null
If index is within the valid range (0 to data.Length-1)
If the string at the given index is not null or empty
If all conditions are met, print "Valid data: " followed by the string at the given index. If any condition fails, print "Invalid access attempt" without throwing exceptions.

Use short-circuit evaluation to ensure safe access to the array and its elements.
}
*/

/*

*/
using System;

class LogicOpAdv5
{
    public static void safeDataAccess(string[] data, int index)
    {
        // Write your code here
        if (data != null && index >= 0 && index < data.Length && !string.IsNullOrWhiteSpace(data[index]))
        {
            Console.WriteLine("Valid data: " + data[index]);
        }
        else
        {
            Console.WriteLine("Invalid access attempt");
        }
    }



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
