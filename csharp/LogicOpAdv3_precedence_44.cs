// Conditional Logical Operators
/*
Here's a simplified precedence order (from highest to lowest):

Parentheses ()
Multiplication/Division * / %
Addition/Subtraction + -
Comparison operators < > <= >=
Equality operators == !=
Logical AND &&
Logical OR ||
Assignment operators = += -= etc.
*/

/*
Create a method named EvaluateExpression that takes three integers (a, b, c) and returns a boolean.

Your method should return the result of this expression:
a > b || a == c && b < c

Then, create another method named EvaluateWithParentheses that evaluates:
(a > b || a == c) && b < c

Your program should read three integers from the console and print the results of both evaluations on separate lines.
*/
using System;

class LogicOpAdv3
{
    public static bool EvaluateExpression(int a, int b, int c)
    {
        // Write your code here
        return a > b || a == c && b < c;
    }

    public static bool EvaluateWithParentheses(int a, int b, int c)
    {
        // Write your code here
        return (a > b || a == c) && b < c;
    }

    public void Main0(string[] args)
    {
        Console.WriteLine("Enter three integers:");
        int a = int.Parse(Console.ReadLine() ?? "0");
        int b = int.Parse(Console.ReadLine() ?? "0");
        int c = int.Parse(Console.ReadLine() ?? "0");

        // Call your methods and print the results
        Console.WriteLine(EvaluateExpression(a, b, c));
        Console.WriteLine(EvaluateWithParentheses(a, b, c));
    }
}
