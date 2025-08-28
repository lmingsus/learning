/*
Create a method named ProcessArray that:

Takes an array of integers and an index as parameters
Tries to access the element at the specified index
Returns the element value if successful
If an IndexOutOfRangeException occurs, catch it and return -1
*/
using System;

class ExceptionHanding
{
    public static int ProcessArray(int[] array, int index)
    {
        // Write your code here
        try
        {
            return array[index];
        }
        catch (IndexOutOfRangeException)
        {
            return -1;
        }
        catch (NullReferenceException)
        {
            return -1;
        }
        catch (Exception)
        {
            // 其他處理
            return -1;
        }
    }

    public void Main0()
    {
        // Read array input
        string input = Console.ReadLine() ?? "[]";

        // Remove brackets if present
        if (input.StartsWith("[") && input.EndsWith("]"))
        {
            input = input.Substring(1, input.Length - 2);
        }

        string[] parts = input.Split(',');

        int[] array = new int[parts.Length];
        for (int i = 0; i < parts.Length; i++)
        {
            array[i] = int.Parse(parts[i].Trim());
        }

        // Read index input
        int index = int.Parse(Console.ReadLine() ?? "0");

        int result = ProcessArray(array, index);
        Console.WriteLine(result);
    }
}