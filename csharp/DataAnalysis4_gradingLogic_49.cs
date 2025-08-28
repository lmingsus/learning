// Data Collection Setup
/*

*/

/*
In this project, you'll build a data analysis system that processes student scores. First, create the foundation for collecting and validating input data.

Now that we can analyze the data, let's implement a grading system to assign letter grades based on the scores. Create a class called GradingSystem with these methods:

1.
ConvertToLetterGrade(double score): Converts a numeric score to a letter grade according to this scale:
A: 90-100
B: 80-89
C: 70-79
D: 60-69
F: 0-59
Invalid: Return "N/A" for any invalid score (negative or > 100)

2.
GetStudentGrade(int[][] scoreGrid, int studentIndex): 
Calculates a student's average and returns their letter grade. Return "N/A" for invalid student indices.

3.
GetClassDistribution(int[][] scoreGrid): 
Returns an array of integers representing the count of each letter grade in the class [A, B, C, D, F].
Base this on the average score of each student.
*/
using System;

class DataCollector4
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


public class DataEntry4
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


public class DataAnalyzer4
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


public class GradingSystem
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