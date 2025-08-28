// Recap - Advanced Operators
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
Create a method called analyzeInput that takes three parameters:

A string text
A nullable integer value
A boolean condition
The method should return a string with the following information:

Check if text is not null and longer than 3 characters (use short-circuit evaluation)
Get the actual value from the nullable integer (or 100 if null) using the null-coalescing operator
Evaluate the expression: condition || text.Length > 5 && value > 50
Evaluate the expression with different precedence: (condition || text.Length > 5) && value > 50
Return the results in this format:

Text valid: {true/false}
Value used: {actualValue}
Expression 1: {result1}
Expression 2: {result2}
*/
using System;

class LogicOpAdv4
{
    public static string analyzeInput(string text, int? value, bool condition)
    {
        bool textValid = !string.IsNullOrEmpty(text) && text.Length > 3;
        int actualValue = value ?? 100;
        bool result1 = condition || (text.Length > 5 && actualValue > 50);
        bool result2 = (condition || text.Length > 5) && actualValue > 50;

        return $@"
                Text valid: {textValid}
                Value used: {actualValue}
                Expression 1: {result1}
                Expression 2: {result2}
                ";
    }
}
