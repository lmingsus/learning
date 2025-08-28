/*
Takes a jagged array of integers (int[][]) and a target value as parameters
Implements four different approaches to find the target value:
Using a traditional for loop without caching array lengths
Using a for loop with cached array lengths
Using a foreach loop with a counter
Using a helper method to check if the value matches the target
Returns the total number of matches found using the optimized approach (with cached lengths)
*/

public class OptimizedLoops
{
    public static int TraditionalSearchAlgorithm(int[][] data, int target)
    {
        // Write your solution here
        int count = 0;
        for (int i = 0; i < data.Length; i++)
        {
            for (int j = 0; j < data[i].Length; j++)
            {
                if (data[i][j] == target)
                {
                    count++;
                }
            }
        }
        return count;
    }

    public static int CachedSearchAlgorithm(int[][] data, int target)
    {
        int count = 0;
        int length = data.Length;
        for (int i = 0; i < length; i++)
        {
            int[] innerArray = data[i];
            int innerLength = innerArray.Length;
            for (int j = 0; j < innerLength; j++)
            {
                if (innerArray[j] == target)
                {
                    count++;
                }
            }
        }
        return count;
    }

    public static int ForeachSearchAlgorithm(int[][] data, int target)
    {
        int count = 0;
        foreach (int[] innerArray in data)
        {
            int innerLength = innerArray.Length;
            foreach (int j in innerArray)
            {
                if (j == target)
                {
                    count++;
                }
            }
        }
        return count;
    }

    void Main0()
    {
        int[][] matrix = new int[][]
        {
            new int[] { 1, 2, 3 },
            new int[] { 4, 5, 6 },
            new int[] { 7, 8, 9 }
        };

        int target = 5;
        int count = TraditionalSearchAlgorithm(matrix, target);
        Console.WriteLine("Traditional Search Count: " + count);
    }

}