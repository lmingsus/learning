// Challenge
/*

*/

/*
Create a method named EvaluateComplexExpression that takes four integers (a, b, c, d) and returns a boolean.

Your method should return the result of this complex expression:
a > b && c < d || a == d && b != c

Then create a method named RewriteWithParentheses that explicitly shows the default operator precedence using parentheses.

Finally, implement AlterPrecedence to evaluate:
(a > b && c < d) || ((a == d) && (b != c))

Your program should read four integers from the console and print the results of all three methods on separate lines.
*/
using System;

class LogicOpAdv7
{
    public static bool EvaluateComplexExpression(int a, int b, int c, int d)
    {
        // Write your code here
        return a > b && c < d || a == d && b != c;
    }

    public static bool RewriteWithParentheses(int a, int b, int c, int d)
    {
        // Write your code here showing default precedence
        return (a > b && c < d) || (a == d && b != c);
    }

    public static bool AlterPrecedence(int a, int b, int c, int d)
    {
        // Write your code here with altered precedence
        return (a > b && c < d) || ((a == d) && (b != c));
    }


    public void Main0(string[] args)
    {
        Console.WriteLine("Enter four integers:");
        int a = int.Parse(Console.ReadLine() ?? "0");
        int b = int.Parse(Console.ReadLine() ?? "0");
        int c = int.Parse(Console.ReadLine() ?? "0");
        int d = int.Parse(Console.ReadLine() ?? "0");

        // Call your methods and print the results
        Console.WriteLine(EvaluateComplexExpression(a, b, c, d));
        Console.WriteLine(RewriteWithParentheses(a, b, c, d));
        Console.WriteLine(AlterPrecedence(a, b, c, d));
    }
}
