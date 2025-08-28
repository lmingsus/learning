// Data Collection Setup
/*

*/

/*
In this project, you'll build a data analysis system that processes student scores. First, create the foundation for collecting and validating input data.

Create a class called DataCollector with these methods:

CreateScoreGrid(int students, int assignments): Creates and returns a jagged array of integers (int[][]) with the specified dimensions to store student scores.
ValidateScore(int score): Returns true if the score is valid (between 0 and 100 inclusive), otherwise false.
PopulateWithDefaultValues(int[][] scoreGrid): Fills the entire grid with a default score of -1 (representing "not graded yet") and returns the updated grid.
IMPORTANT: Do not modify the test code at the bottom of the file. It will be used to validate your implementation.
*/
using System;

class DataAnalysis1
{
    public static int[][] CreateScoreGrid(int students, int assignments)
    {
        int[][] scoreGrid = new int[students][];
        for (int i = 0; i < students; i++)
        {
            scoreGrid[i] = new int[assignments];
        }
        return scoreGrid;
    }

    public static bool ValidateScore(int score)
    {
        return score >= 0 && score <= 100;
    }

    public static int[][] PopulateWithDefaultValues(int[][] scoreGrid)
    {
        for (int i = 0; i < scoreGrid.Length; i++)
        {
            for (int j = 0; j < scoreGrid[i].Length; j++)
            {
                scoreGrid[i][j] = -1; // Default value representing "not graded yet"
            }
        }
        return scoreGrid;
    }
}
