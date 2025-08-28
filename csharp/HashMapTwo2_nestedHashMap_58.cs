// Declare a HashMap
/*
Dictionary<string, int> fruitInventory = new Dictionary<string, int>();
fruitInventory.Add("Apple", 10);
fruitInventory.Add("Banana", 15);


Dictionary<string, int> fruitInventory = new Dictionary<string, int>()
{
    { "Apple", 10 },
    { "Banana", 15 }
};

bool exists = fruitInventory.ContainsKey("Apple");

int appleCount = fruitInventory["Apple"];  // key that doesn't exist, you'll get a KeyNotFoundException.

Update an existing key's value:
if (inventory.ContainsKey("apple"))
{
    inventory["apple"] = 15;  // Updates "apple" to have value 15
}

Remove a key-value pair:
inventory.Remove("apple");
inventory.Remove("orange");    // It returns false and doesn't modify the dictionary:

Clear all entries: Remove all key-value pairs
inventory.Clear();

Get all keys
Dictionary<string, int>.KeyCollection keys = inventory.Keys;
foreach (string name in keys)
{
    Console.WriteLine(name);
}

Get all values
Dictionary<string, int>.ValueCollection values = inventory.Values;
foreach (int value in values)
{
    Console.WriteLine(value);
}
*/


/*
Create a method named AddCourseGrade that takes four arguments:

A nested Dictionary representing student grades: Dictionary<string, Dictionary<string, int>> grades
A student name (string)
A course name (string)
A grade (int)
The method should:

If the student doesn't exist in the dictionary, create a new entry for them
Add the course and grade to the student's record
If the course already exists for that student, update the grade
Print "Added [course] grade for [student]: [grade]" after adding/updating
*/


/*

*/

using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

class HashMap7
{
    public static void AddCourseGrade(Dictionary<string, Dictionary<string, int>> grades, string student, string course, int grade)
    {
        // Write your code here
        if (!grades.ContainsKey(student))
        {
            grades[student] = new Dictionary<string, int>();
        }
        grades[student][course] = grade;
        Console.WriteLine($"Added {course} grade for {student}: {grade}");
    }


    static void Main(string[] args)
    {
        // Check if first line might be JSON
        string firstLine = Console.ReadLine();

        Dictionary<string, Dictionary<string, int>> studentGrades = new Dictionary<string, Dictionary<string, int>>();
        string student = ""; // Initialize student
        string course = ""; // Initialize course
        int grade = 0; // Initialize grade

        // JSON format input
        if (firstLine != null && firstLine.StartsWith("{") && firstLine.EndsWith("}"))
        {
            try
            {
                // Parse existing student grades from JSON
                string jsonContent = firstLine.Substring(1, firstLine.Length - 2);
                string studentPattern = @"""([^""]+)""\s*:\s*\{([^\}]+)\}";

                MatchCollection studentMatches = Regex.Matches(jsonContent, studentPattern);
                foreach (Match studentMatch in studentMatches)
                {
                    string studentName = studentMatch.Groups[1].Value;
                    string coursesJson = studentMatch.Groups[2].Value;

                    Dictionary<string, int> courseGrades = new Dictionary<string, int>();
                    string coursePattern = @"""([^""]+)""\s*:\s*(\d+)";

                    MatchCollection courseMatches = Regex.Matches(coursesJson, coursePattern);
                    foreach (Match courseMatch in courseMatches)
                    {
                        string courseName = courseMatch.Groups[1].Value;
                        int courseGrade = int.Parse(courseMatch.Groups[2].Value);
                        courseGrades.Add(courseName, courseGrade);
                    }

                    studentGrades.Add(studentName, courseGrades);
                }

                // Parse student, course, and grade for the operation
                string studentInput = Console.ReadLine();
                Match studentNameMatch = Regex.Match(studentInput, @"""([^""]+)""");
                student = studentNameMatch.Success ? studentNameMatch.Groups[1].Value : studentInput;

                string courseInput = Console.ReadLine();
                Match courseNameMatch = Regex.Match(courseInput, @"""([^""]+)""");
                course = courseNameMatch.Success ? courseNameMatch.Groups[1].Value : courseInput;

                grade = int.Parse(Console.ReadLine());
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error parsing JSON input: {ex.Message}");
                return;
            }
        }
        AddCourseGrade(studentGrades, student, course, grade);
    }
}