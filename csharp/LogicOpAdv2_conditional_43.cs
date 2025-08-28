// Conditional Logical Operators
/*
The two main conditional logical operators are ?? (null-coalescing) and ?. (null-conditional).

Use the null-coalescing operator to provide a default value:
string displayName = name ?? "Guest";
}
*/

/*
Create a method named getSafeValue that takes two arguments:

A nullable integer (int? value)
An integer (int defaultValue)
The method should return the value if it's not null, otherwise it should return the defaultValue. Use the null-coalescing operator (??) to achieve this.
*/
using System;

class LogicOpAdv2
{
    public static int getSafeValue(int? value, int defaultValue)
    {
        // Write your code here
        return value ?? defaultValue;
    }
}
