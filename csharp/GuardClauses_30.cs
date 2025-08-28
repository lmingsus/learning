public class GuardClauses
{
    static int DivideNumbers(int numerator, int denominator)
    {
        // Write your code here
        if (denominator == 0)
        {
            Console.WriteLine("Cannot divide by zero");
            return 0;
        }
        return numerator / denominator;
    }

    public void Main0()
    {
        // Read inputs from console
        int numerator = Convert.ToInt32(Console.ReadLine());
        int denominator = Convert.ToInt32(Console.ReadLine());

        // Call the DivideNumbers method
        int result = DivideNumbers(numerator, denominator);

        // Print the result
        Console.WriteLine(result);
    }
}