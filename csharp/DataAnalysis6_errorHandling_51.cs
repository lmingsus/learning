// Data Collection Setup
/*

*/

/*
In this project, you'll build a data analysis system that processes student scores. First, create the foundation for collecting and validating input data.

Let's enhance our system with robust error handling to deal with potential issues gracefully. Create a class called ErrorHandler with these methods:

1.
ValidateInput(int[][] scoreGrid, int studentIndex, int assignmentIndex): Validates the input indices and returns an appropriate error message or an empty string if valid.
Returns "Invalid student index" if the student index is out of bounds.
Returns "Invalid assignment index" if the assignment index is out of bounds.
Returns an empty string "" if both indices are valid.

2.
SafeGetScore(int[][] scoreGrid, int studentIndex, int assignmentIndex): Safely retrieves a score with error handling.
Returns the score if both indices are valid.
Returns -999 if any index is invalid.

3.
ProcessBatchUpdate(int[][] scoreGrid, int[][] updates): Processes batch updates where each update is [studentIndex, assignmentIndex, score].
Returns a string array of error messages for each failed update.
Format: "Error at index X: [specific error message]"
Return an empty array if all updates are successful.
*/
using System;

class DataCollector6
{
    public static int[][] CreateScoreGrid(int students, int assignments)
    {
        // Write your code here
        int[][] scoreGrid = new int[students][];
        for (int i = 0; i < students; i++)
        {
            scoreGrid[i] = new int[assignments];
        }
        return scoreGrid;
    }

    public static bool ValidateScore(int score)
    {
        // Write your code here
        return score >= 0 && score <= 100;
    }

    public static int[][] PopulateWithDefaultValues(int[][] scoreGrid)
    {
        // Write your code here
        for (int i = 0; i < scoreGrid.Length; i++)
        {
            for (int j = 0; j < scoreGrid[i].Length; j++)
            {
                scoreGrid[i][j] = -1;
            }
        }
        return scoreGrid;
    }
}


public class DataEntry6
{
    public static int SetStudentScore(int[][] scoreGrid, int studentIndex, int assignmentIndex, int score)
    {
        if (!DataCollector3.ValidateScore(score))
        {
            return -2;
        }
        if (studentIndex < scoreGrid.Length && assignmentIndex < scoreGrid[studentIndex].Length)
        {
            scoreGrid[studentIndex][assignmentIndex] = score;
            return 0;
        }
        else
        {
            return -1;
        }
    }

    public static int UpdateAllScores(int[][] scoreGrid, int[] studentIndices, int assignmentIndex, int score)
    {
        int updatedCount = 0;
        if (!DataCollector2.ValidateScore(score))
        {
            return -2;
        }
        foreach (int studentIndex in studentIndices)
        {
            if (studentIndex < scoreGrid.Length && assignmentIndex < scoreGrid[studentIndex].Length)
            {
                scoreGrid[studentIndex][assignmentIndex] = score;
                updatedCount++;
            }
        }
        return updatedCount;
    }
}


public class DataAnalyzer6
{
    public static double CalculateStudentAverage(int[][] scoreGrid, int studentIndex)
    {
        if (studentIndex >= scoreGrid.Length || studentIndex < 0)
        {
            return -1;
        }
        double sum = 0;
        int count = 0;
        foreach (int score in scoreGrid[studentIndex])
        {
            sum += score != -1 ? score : 0;
            count += score != -1 ? 1 : 0;
        }
        return count != 0 ? sum / count : 0;
    }

    public static double CalculateAssignmentAverage(int[][] scoreGrid, int assignmentIndex)
    {
        if (assignmentIndex >= scoreGrid[0].Length || assignmentIndex < 0)
        {
            return -1;
        }
        double sum = 0;
        int count = 0;
        for (int i = 0; i < scoreGrid.Length; i++)
        {
            sum += scoreGrid[i][assignmentIndex] != -1 ? scoreGrid[i][assignmentIndex] : 0;
            count += scoreGrid[i][assignmentIndex] != -1 ? 1 : 0;
        }
        return count != 0 ? sum / count : 0;
    }

    public static int[] FindHighestScore(int[][] scoreGrid)
    {
        int studentIndex = 0, assignmentIndex = 0, score = 0;
        for (int i = 0; i < scoreGrid.Length; i++)
        {
            for (int j = 0; j < scoreGrid[i].Length; j++)
            {
                if (scoreGrid[i][j] > score)
                {
                    score = scoreGrid[i][j];
                    studentIndex = i;
                    assignmentIndex = j;
                }
            }
        }
        return new int[] { studentIndex, assignmentIndex, score };
    }
}


public class GradingSystem6
{
    public static string ConvertToLetterGrade(double score)
    {
        // switch (score)
        // {
        //     case > 100:
        //     case < 0:
        //         return "N/A";
        //     case >= 90:
        //         return "A";
        //     case >= 80:
        //         return "B";
        //     case >= 70:
        //         return "C";
        //     case >= 60:
        //         return "D";
        //     case >= 0:
        //         return "F";
        //     default:
        //         return "N/A";
        // }

        // return score switch
        // {
        //     > 100 or < 0 => "N/A",
        //     >= 90 => "A",
        //     >= 80 => "B",
        //     >= 70 => "C",
        //     >= 60 => "D",
        //     >= 0 => "F",
        //     _ => "N/A",
        // };

        if (score < 0 || score > 100)
        {
            return "N/A";
        }
        else if (score >= 90)
        {
            return "A";
        }
        else if (score >= 80)
        {
            return "B";
        }
        else if (score >= 70)
        {
            return "C";
        }
        else if (score >= 60)
        {
            return "D";
        }
        else
        {
            return "F";
        }
    }

    public static string GetStudentGrade(int[][] scoreGrid, int studentIndex)
    {
        if (studentIndex > scoreGrid.Length || studentIndex < 0)
        {
            return "N/A";
        }
        double sum = 0;
        int count = 0;
        foreach (int score in scoreGrid[studentIndex])
        {
            sum += score != -1 ? score : 0;
            count += score != -1 ? 1 : 0;
        }
        return ConvertToLetterGrade(sum / count);
    }

    public static int[] GetClassDistribution(int[][] scoreGrid)
    {
        int[] gradeCount = new int[5];
        for (int i = 0; i < scoreGrid.Length; i++)
        {
            switch (GetStudentGrade(scoreGrid, i))
            {
                case "A":
                    gradeCount[0]++;
                    break;
                case "B":
                    gradeCount[1]++;
                    break;
                case "C":
                    gradeCount[2]++;
                    break;
                case "D":
                    gradeCount[3]++;
                    break;
                case "F":
                    gradeCount[4]++;
                    break;
                default:
                    break;
            }
        }
        return gradeCount;
    }
}

public class ReportGenerator6
{
    public static string GenerateStudentReport(int[][] scoreGrid, int studentIndex)
    {
        if (studentIndex < 0 || studentIndex >= scoreGrid.Length)
        {
            return "Invalid student index";
        }

        double average = DataAnalyzer5.CalculateStudentAverage(scoreGrid, studentIndex);
        string grade = GradingSystem5.GetStudentGrade(scoreGrid, studentIndex);
        string scores = string.Join(", ", Array.ConvertAll(scoreGrid[studentIndex], s => s == -1 ? "N/A" : s.ToString()));

        return $"Student #{studentIndex + 1} | Average: {average:F1} | Grade: {grade}\nAssignment scores: {scores}";
    }

    public static string GenerateClassSummary(int[][] scoreGrid)
    {
        int totalStudents = scoreGrid.Length;
        double totalAverage = 0;
        for (int i = 0; i < totalStudents; i++)
        {
            totalAverage += DataAnalyzer5.CalculateStudentAverage(scoreGrid, i);
        }
        totalAverage /= totalStudents;

        int[] distribution = GradingSystem5.GetClassDistribution(scoreGrid);
        return $"Class Summary\nTotal Students: {totalStudents}\nClass Average: {totalAverage:F1}\nGrade Distribution: A: {distribution[0]}, B: {distribution[1]}, C: {distribution[2]}, D: {distribution[3]}, F: {distribution[4]}";
    }

    public static string GenerateAssignmentReport(int[][] scoreGrid, int assignmentIndex)
    {
        if (assignmentIndex < 0 || assignmentIndex >= scoreGrid[0].Length)
        {
            return "Invalid assignment index";
        }

        double average = DataAnalyzer5.CalculateAssignmentAverage(scoreGrid, assignmentIndex);
        int completedCount = 0;
        foreach (var studentScores in scoreGrid)
        {
            if (studentScores[assignmentIndex] != -1)
            {
                completedCount++;
            }
        }
        double completionRate = (double)completedCount / scoreGrid.Length * 100;

        return $"Assignment #{assignmentIndex + 1} | Average: {average:F1} | Completion Rate: {completionRate:F1}%";
    }
}

public class ErrorHandler
{
    public static string ValidateInput(int[][] scoreGrid, int studentIndex, int assignmentIndex)
    {
        if (studentIndex < 0 || studentIndex >= scoreGrid.Length)
        {
            return "Invalid student index";
        }
        if (assignmentIndex < 0 || assignmentIndex >= scoreGrid[studentIndex].Length)
        {
            return "Invalid assignment index";
        }
        return "";
    }

    public static int SafeGetScore(int[][] scoreGrid, int studentIndex, int assignmentIndex)
    {
        string validationResult = ValidateInput(scoreGrid, studentIndex, assignmentIndex);
        if (!string.IsNullOrEmpty(validationResult))
        {
            return -999;
        }
        return scoreGrid[studentIndex][assignmentIndex];
    }

    public static string[] ProcessBatchUpdate(int[][] scoreGrid, int[][] updates)
    {
        // List<string> errorMessages = new List<string>();
        // foreach (var update in updates)
        // {
        //     if (update.Length != 3)
        //     {
        //         errorMessages.Add($"Error at index {Array.IndexOf(updates, update)}: Invalid update format");
        //         continue;
        //     }
        //     int studentIndex = update[0];
        //     int assignmentIndex = update[1];
        //     int newScore = update[2];

        //     string validationResult = ValidateInput(scoreGrid, studentIndex, assignmentIndex);
        //     if (!string.IsNullOrEmpty(validationResult))
        //     {
        //         errorMessages.Add($"Error at index {Array.IndexOf(updates, update)}: {validationResult}");
        //         continue;
        //     }

        //     scoreGrid[studentIndex][assignmentIndex] = newScore;
        // }
        // return errorMessages.ToArray();

        string[] errorMessages = new string[updates.Length];
        int errorCount = 0;
        foreach (var update in updates)
        {
            if (update.Length != 3)
            {
                continue;
            }
            string validString = ValidateInput(scoreGrid, update[0], update[1]);
            if (validString != "")
            {
                errorMessages[errorCount] = $"Error at index {Array.IndexOf(updates, update)}: {validString}";
                errorCount++;
                continue;
            }
            int score = update[2];
            if (score < 0 || score > 100)
            {
                errorMessages[errorCount] = $"Error at index {Array.IndexOf(updates, update)}: Invalid score value";
                errorCount++;
                continue;
            }
            scoreGrid[update[0]][update[1]] = score;
        }
        string[] returnArray = new string[errorCount];
        Array.Copy(errorMessages, 0, returnArray, 0, errorCount);

        return returnArray;
    }
}
