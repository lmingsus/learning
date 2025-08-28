using System;

// To create a custom exception, define a class that inherits from Exception:
public class InvalidAgeException : Exception
{
    public InvalidAgeException() : base("Age is not valid.")  // default 
    {
    }

    public InvalidAgeException(string message) : base(message)
    {
    }
}


class CheckTemperature
{
    // Create your custom exception class here
    public class InvalidTemperatureException : Exception
    {
        public InvalidTemperatureException() : base("Temperature is not valid.")
        {
        }
        public InvalidTemperatureException(string message) : base(message)
        {
        }
    }

    public static bool checkTemperature(int celsius)
    {
        // Write your code here
        if (celsius < -273)
        {
            throw new InvalidAgeException("Temperature below absolute zero!");
        }
        return true;
    }

}