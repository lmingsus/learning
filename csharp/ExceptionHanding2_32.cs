/*
Create a method named DivideNumbers that takes two string parameters:

numeratorStr: a string representing the numerator
denominatorStr: a string representing the denominator

The method should:

Try to parse both strings to integers
Try to divide the numerator by the denominator
Return the result as an integer
Handle FormatException by printing "Invalid format" and returning 0
Handle DivideByZeroException by printing "Cannot divide by zero" and returning 0
Handle any other exceptions with a general catch block that prints "An error occurred" and returning 0
*/
using System;

class ExceptionHanding2
{
    public static int DivideNumbers(string numeratorStr, string denominatorStr)
    {
        // Write your code here
        try
        {
            int numerator = int.Parse(numeratorStr);
            int denominator = int.Parse(denominatorStr);
            return numerator / denominator;
        }
        catch (FormatException)
        {
            Console.WriteLine("Invalid format");
            return 0;
        }
        catch (DivideByZeroException)
        {
            Console.WriteLine("Cannot divide by zero");
            return 0;
        }
        catch (Exception)
        {
            Console.WriteLine("An error occurred");
            return 0;
        }
    }

    public void Main0()
    {
        string numeratorStr = Console.ReadLine() ?? "0";
        string denominatorStr = Console.ReadLine() ?? "0";

        int result = DivideNumbers(numeratorStr, denominatorStr);
        Console.WriteLine("Result: " + result);
    }
}