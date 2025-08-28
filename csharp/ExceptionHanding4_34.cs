// Using vs. Try-Finally
/*
Create a method named processFile that:

Takes a filename as a string parameter
Uses the using statement with a StreamReader to read all lines from the file
Returns the number of lines in the file
If a FileNotFoundException occurs, print "File not found" and return -1
*/
using System;
using System.IO;

class ExceptionHanding4
{
    public static int ProcessFile(string filename)
    {
        try
        {
            int lineCount = 0;
            using (StreamReader reader = new StreamReader(filename))
            {
                while (reader.ReadLine() != null)
                {
                    lineCount++;
                }
            }
            return lineCount;
        }
        catch (FileNotFoundException)
        {
            Console.WriteLine("File not found");
            return -1;
        }
    }
}
