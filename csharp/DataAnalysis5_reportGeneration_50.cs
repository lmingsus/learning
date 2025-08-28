// Data Collection Setup
/*

*/

/*
In this project, you'll build a data analysis system that processes student scores. First, create the foundation for collecting and validating input data.

Now that we have the grading system, let's create a reporting module to generate formatted reports about student performance. Create a class called ReportGenerator with these methods:

1.
GenerateStudentReport(int[][] scoreGrid, int studentIndex): 
Returns a formatted string reporting a specific student's scores, average, and letter grade.
Format: "Student #X | Average: YY.Y | Grade: Z\nAssignment scores: A, B, C, ...".
For ungraded assignments (score of -1), display "N/A" instead of the score.
Return "Invalid student index" for any invalid student index.

2.
GenerateClassSummary(int[][] scoreGrid):
Returns a formatted string summarizing the class performance.
Format: "Class Summary\nTotal Students: X\nClass Average: YY.Y\nGrade Distribution: A: #, B: #, C: #, D: #, F: #"

3.
GenerateAssignmentReport(int[][] scoreGrid, int assignmentIndex):
Returns a formatted string with statistics for a specific assignment.
Format: "Assignment #X | Average: YY.Y | Completion Rate: Z%"
Completion rate is the percentage of students who have a grade for this assignment (not -1).
Return "Invalid assignment index" for any invalid assignment index.
*/
using System;

class DataCollector5
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


public class DataEntry5
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


public class DataAnalyzer5
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


public class GradingSystem5
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

public class ReportGenerator
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