// Challenge: Finally Block
/*
Create a method named processTransaction that:

Takes a string parameter representing a transaction ID
Simulates opening a database connection (just print "Opening connection")
If the transaction ID is "invalid", throw an ArgumentException with message "Invalid transaction ID"
If the transaction ID is "error", throw a new Exception with message "Processing error"
For any other ID, print "Processing transaction: [ID]"
Always ensure the connection is closed in a finally block (print "Connection closed")
Handle exceptions appropriately and print error messages in this format: "ERROR: [exception message]"
*/
using System;
using System.IO;

class ExceptionHanding7
{
    public static void processTransaction(string transactionId)
    {
        Console.WriteLine("Opening connection");
        try
        {
            if (transactionId == "invalid")
            {
                throw new ArgumentException("Invalid transaction ID");
            }
            if (transactionId == "error")
            {
                throw new Exception("Processing error");
            }
            Console.WriteLine($"Processing transaction: {transactionId}");
        }
        catch (ArgumentException ex)
        {
            Console.WriteLine($"ERROR: {ex.Message}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"ERROR: {ex.Message}");
        }
        finally
        {
            Console.WriteLine("Connection closed");
        }
    }

}
