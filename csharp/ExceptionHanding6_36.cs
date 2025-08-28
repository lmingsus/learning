// Recap - Error Handling
/*
Create a method called processUserData that:

Takes two parameters: a string filePath and an int userAge
Uses a using statement to read the first line from the file at filePath
Verifies that userAge is between 18 and 120 (inclusive)
If the age is invalid, throw a custom exception called InvalidUserAgeException with the message "Age must be between 18 and 120"
If the file doesn't exist, catch the FileNotFoundException and print "User file not found"
If another IO exception occurs, catch it and print "Error reading user data: [exception message]"
For any other exceptions, print "An unexpected error occurred"
Return the file content if successful or "No data" if any exception occurs
*/
using System;
using System.IO;

class ExceptionHanding6
{
    // Create your custom exception here
    public class InvalidUserAgeException : Exception
    {
        public InvalidUserAgeException() : base()
        {
        }
        public InvalidUserAgeException(string message) : base(message)
        {
        }
    }

    public static string processUserData(string filePath, int userAge)
    {
        // Write your code here
        string? line = "";
        try
        {
            if (userAge < 18 || userAge > 120)
            {
                throw new InvalidUserAgeException("Age must be between 18 and 120");
            }
            using (StreamReader reader = new StreamReader(filePath))
            {
                line = reader.ReadLine();
            }
        }
        catch (InvalidUserAgeException ex)
        {
            Console.WriteLine(ex.Message);
        }
        catch (FileNotFoundException)
        {
            Console.WriteLine("User file not found");
        }
        catch (IOException ex)
        {
            Console.WriteLine($"Error reading user data: {ex.Message}");
        }
        catch (Exception)
        {
            Console.WriteLine("An unexpected error occurred");
        }

        return line ?? "No data";
    }
}
