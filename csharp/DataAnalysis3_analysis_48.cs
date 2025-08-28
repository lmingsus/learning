// Data Collection Setup
/*

*/

/*
In this project, you'll build a data analysis system that processes student scores. First, create the foundation for collecting and validating input data.

Now that we have our data structure, let's implement logic for entering and updating student scores.

Create a class called DataEntry with these methods:

SetStudentScore(int[][] scoreGrid, int studentIndex, int assignmentIndex, int score): Sets the score for a specific student and assignment if it's valid. Returns:
0 if successful
-1 if any index is out of bounds
-2 if the score is invalid

UpdateAllScores(int[][] scoreGrid, int[] studentIndices, int assignmentIndex, int score): Updates scores for multiple students on the same assignment. Returns the number of successfully updated scores.

Note: Use the ValidateScore method from the DataCollector class to check score validity.
*/
using System;

class DataCollector3
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


public class DataEntry3
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


public class DataAnalyzer
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