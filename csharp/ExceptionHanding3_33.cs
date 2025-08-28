/*
Create a method named ProcessData that:

Takes a string parameter representing a filename
Attempts to open the file and read its contents
Writes the contents to the console
Properly cleans up resources using a finally block
Handles FileNotFoundException and IOException

If the file can't be found, print: "ERROR: File not found: [filename]"

If another IO error occurs, print: "ERROR: Could not read the file: [error message]"

Always print "File operation completed." in the finally block, whether an exception occurred or not.
*/
using System;
using System.IO;

class ExceptionHanding3
{
    public static void ProcessData(string filename)
    {
        // Write your code here
        StreamReader? file = null;
        try
        {
            file = new StreamReader(filename);
            string content = file.ReadToEnd();
            Console.WriteLine(content);
        }
        catch (FileNotFoundException)
        {
            Console.WriteLine($"ERROR: File not found: {filename}");
        }
        catch (IOException ex)
        {
            Console.WriteLine($"ERROR: Could not read the file: {ex.Message}");
        }
        finally
        {
            Console.WriteLine("File operation completed.");
        }
    }


    public void Main0()
    {
        string filename = Console.ReadLine() ?? "";
        ProcessData(filename);
    }
}